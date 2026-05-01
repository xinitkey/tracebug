import jwt
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


# Generation hashed pasword
def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


# Verify generated hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)
