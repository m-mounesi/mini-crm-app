from repositories.rbac_repository import RBACRepository
from models.user_role import UserRoleDB


class RBACService:
    def __init__(self):
        self.repo = RBACRepository()

    def build_user_context(self, db, user_id: int):
        roles = [r[0] for r in self.repo.get_user_roles(db, user_id)]
        permissions = [p[0] for p in self.repo.get_user_permissions(db, user_id)]

        return {"roles": roles, "permissions": permissions}

    def assign_role(self, db, user_id: int, role_name: str):
        role = self.repo.get_role_by_name(db, role_name)
        if not role:
            raise ValueError("Role not found")

        exists = self.repo.user_has_role(db, user_id, role.id)

        exists = (
            db.query(UserRoleDB)
            .filter(UserRoleDB.user_id == user_id, UserRoleDB.role_id == role.id)
            .first()
        )

        if exists:
            return exists

        user_role = UserRoleDB(user_id=user_id, role_id=role.id)
        db.add(user_role)
        db.commit()

        return user_role
