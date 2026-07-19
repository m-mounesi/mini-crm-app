from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.database import get_db
from core.exceptions import UnauthorizedException
from security.jwt import decode_access_token
from services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
service = AuthService()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    if not payload:
        raise UnauthorizedException("Invalid token")

    username = payload.get("sub")
    if username is None:
        raise UnauthorizedException("Invalid token: missing username")

    user = service.get_user(db, username)  # Ensure the user exists in the database
    if user is None:
        raise UnauthorizedException("User not found")

    return user
