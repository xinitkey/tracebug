from fastapi import APIRouter
from pydantic import BaseModel


class Auth(BaseModel):
    name: str
    age: int


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/auth")
async def login(auth: Auth):
    return auth
