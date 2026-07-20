from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import UserDB
from security.auth import get_current_user
from core.dependencies import get_auth_service
from services.auth_service import AuthService


def require_permission(permission: str):
    def checker(
        user: UserDB = Depends(get_current_user),
        db: Session = Depends(get_db),
        service: AuthService = Depends(get_auth_service),
    ):
        allowed = get_auth_service.has_perrmisson(db, user.user_id, permission)

        if not allowed:
            raise HTTPException(status_code=403, detail="Permission denied")

        return user

    return checker
