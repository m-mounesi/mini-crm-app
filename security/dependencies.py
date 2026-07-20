from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from repositories.rbac_repository import RBACRepository
from security.auth import get_current_user
from core.exceptions import PermissionDeniedException


def require_permission(permission: str):
    def permission_checker(
        current_user=Depends(get_current_user), db: Session = Depends(get_db)
    ):
        repo = RBACRepository()
        permissions = repo.get_user_permissions(db, current_user.user_id)
        permission_names = [p[0] for p in permissions]
        has_access = permission in permission_names

        if not has_access:
            raise PermissionDeniedException(
                "You do not have permission to perform this action."
            )

        return current_user

    return permission_checker
