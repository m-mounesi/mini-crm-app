from models.user_role import UserRole
from models.role_permission import RolePermission
from models.role import Role
from models.permission import Permission


class RBACRepository:
    def get_user_roles(self, db, user_id: int):
        return (
            db.query(Role.name).join(UserRole).filter(UserRole.user_id == user_id).all()
        )

    def get_user_permissions(self, db, user_id: int):
        return (
            db.query(Permission.name)
            .join(RolePermission)
            .join(Role)
            .join(UserRole)
            .filter(UserRole.user_id == user_id)
            .all()
        )
