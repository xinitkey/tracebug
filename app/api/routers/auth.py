from fastapi import APIRouter
from app.schemas.user import UserCreate
from app.services.user import create_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/auth/register")
async def register(data: UserCreate):
    user = create_user(data)
    return user
