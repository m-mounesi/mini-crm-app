from repositories.rbac_repository import RBACRepository


class RBACManagementService:
    def __init__(self):
        self.repo = RBACRepository()

    def assign_role(self, db, user_id, role_name):
        role = self.repo.get_role_by_name(db, role_name)

        if not role:
            return None

        return self.repo.assign_role_to_user(db, user_id, role.id)

    def assign_permission(self, db, role_name, permission_name):
        role = self.repo.get_role_by_name(db, role_name)

        permission = self.repo.get_permission_by_name(db, permission_name)

        if not role or not permission:
            return None

        return self.repo.assign_permission_to_role(db, role.id, permission.id)
