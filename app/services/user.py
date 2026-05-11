from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import UserModel
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.core.security import verify_password


def create_user(data: UserCreate) -> UserModel:
    hashed_password = get_password_hash(data.password)

    user = UserModel(
        email=data.email,
        username=data.username,
        hashed_password=hashed_password,
    )
    return user


async def get_user(username: str, session: AsyncSession) -> UserModel | None:
    stmt = select(UserModel).where(UserModel.username == username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    return user


async def authenticate_user(
    username: str, password: str, session: AsyncSession
) -> UserModel | None:
    user = await get_user(username, session)
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
