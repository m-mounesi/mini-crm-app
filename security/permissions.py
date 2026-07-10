from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from security.auth import get_current_user
from services.authorization_service import AuthorizationService


service = AuthorizationService()


def require_permission(permission: str):
    def checker(user=Depends(get_current_user), db: Session = Depends(get_db)):
        allowed = service.has_permission(db, user["user_id"], permission)

        if not allowed:
            raise HTTPException(status_code=403, detail="Permission denied")

        return user

    return checker
