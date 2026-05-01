from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def create_user(data: UserCreate) -> User:
    hashed_password = get_password_hash(data.password)

    user = User(
        email=data.email,
        username=data.username,
        hashed_password=hashed_password,
    )
    return user
