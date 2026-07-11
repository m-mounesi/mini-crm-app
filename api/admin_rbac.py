from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from services.rbac_management_service import RBACManagementService
from security.permissions import require_permission


router = APIRouter(prefix="/admin/rbac", tags=["RBAC"])


service = RBACManagementService()


# Assign Role to User


@router.post(
    "/users/{user_id}/roles", dependencies=[Depends(require_permission("user.manage"))]
)
def assign_role(user_id: int, role_name: str, db: Session = Depends(get_db)):
    result = service.assign_role(db, user_id, role_name)
    if result is None:
        return {"message": "role or user not found"}

    return {"message": "role assigned"}


# Assign Permission to Role
@router.post(
    "/roles/{role_name}/permissions",
    dependencies=[Depends(require_permission("user.manage"))],
)
def assign_permission(
    role_name: str, permission_name: str, db: Session = Depends(get_db)
):
    result = service.assign_permission(db, role_name, permission_name)

    if result is None:
        return {"message": "role or permission not found"}

    return {"message": "permission assigned"}
