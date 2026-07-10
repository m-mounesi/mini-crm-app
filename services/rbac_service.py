from repositories.rbac_repository import RBACRepository
from models.user_role import UserRole
from models.role import Role


class RBACService:
    def __init__(self):
        self.repo = RBACRepository()

    def build_user_context(self, db, user_id: int):
        roles = [r[0] for r in self.repo.get_user_roles(db, user_id)]
        permissions = [p[0] for p in self.repo.get_user_permissions(db, user_id)]

        return {"roles": roles, "permissions": permissions}

    def assign_role(self, db, user_id: int, role_name: str):
        role = db.query(Role).filter(Role.name == role_name).first()

        if not role:
            return None

        exists = (
            db.query(UserRole)
            .filter(UserRole.user_id == user_id, UserRole.role_id == role.id)
            .first()
        )

        if exists:
            return exists

        user_role = UserRole(user_id=user_id, role_id=role.id)
        db.add(user_role)
        db.commit()

        return user_role
