from repositories.rbac_repository import RBACRepository


class AuthorizationService:
    def __init__(self):
        self.repo = RBACRepository()

    def has_permission(self, db, user_id: int, permission: str):
        permissions = self.repo.get_user_permissions(db, user_id)

        permission_names = [p[0] for p in permissions]

        return permission in permission_names
