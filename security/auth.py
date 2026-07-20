from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.database import get_db
from core.exceptions import UnauthorizedException
from security.jwt import decode_access_token
from repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    if not payload:
        raise UnauthorizedException("Invalid token")

    username = payload.get("sub")
    if username is None:
        raise UnauthorizedException("Invalid token: missing username")

    repo = UserRepository()
    user = repo.get_user(db, username)

    if user is None:
        raise UnauthorizedException("User not found")

    return user
