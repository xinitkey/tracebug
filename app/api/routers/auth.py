from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from sqlalchemy import or_, select

from app.db.models.user import UserModel
from app.db.session import SessionDep
from app.schemas.auth import Token, TokenData
from app.schemas.user import UserCreate, UserRead
from app.services.user import (
    authenticate_user,
    create_user,
    get_user as get_user_by_username,
)
from app.core.security import (
    ACCESS_TOKEN_EXPIRES_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, session: SessionDep):
    stmt = select(UserModel).where(
        or_(
            UserModel.username == data.username,
            UserModel.email == data.email,
        )
    )
    result = await session.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        if existing_user.username == data.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already exists",
            )

        if existing_user.email == data.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

    new_user = create_user(data)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
    response: Response,
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(key=access_token, value="bearer")
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    token_data = TokenData(username=username)
    if token_data.username is None:
        raise credentials_exception

    user = await get_user_by_username(token_data.username, session)
    if user is None:
        raise credentials_exception
    return user


@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    return current_user


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: SessionDep):
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
