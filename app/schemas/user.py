from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    username: str
    email: str | None = None

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    username: str = Field(min_length=5, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
