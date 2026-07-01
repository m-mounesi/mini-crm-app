from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from security.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "user_id": payload["user_id"],
        "username": payload["sub"],
        "role": payload.get("role", "user"),
    }
