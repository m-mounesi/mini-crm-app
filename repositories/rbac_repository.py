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

    def get_role_by_name(self, db, name):
        return db.query(Role).filter(Role.name == name).first()

    def get_permission_by_name(self, db, name):
        return db.query(Permission).filter(Permission.name == name).first()

    def assign_role_to_user(self, db, user_id, role_id):
        obj = UserRole(user_id=user_id, role_id=role_id)

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    def assign_permission_to_role(self, db, role_id, permission_id):
        obj = RolePermission(role_id=role_id, permission_id=permission_id)

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj
