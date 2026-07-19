from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from security.auth import get_current_user
from services.authorization_service import AuthorizationService
from core.exceptions import PermissionDeniedException


authorization_service = AuthorizationService()


def require_permission(permission: str):
    def permission_checker(
        current_user=Depends(get_current_user), db: Session = Depends(get_db)
    ):
        has_access = authorization_service.has_permission(
            db=db, user_id=current_user.id, permission=permission
        )

        if not has_access:
            raise PermissionDeniedException(
                "You do not have permission to perform this action."
            )

        return current_user

    return permission_checker
