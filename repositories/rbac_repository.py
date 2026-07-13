from models.user_role import UserRoleDB
from models.role_permission import RolePermissionDB
from models.role import RoleDB
from models.permission import PermissionDB


class RBACRepository:
    def get_user_roles(self, db, user_id: int):
        return (
            db.query(RoleDB.name)
            .join(UserRoleDB)
            .filter(UserRoleDB.user_id == user_id)
            .all()
        )

    def get_user_permissions(self, db, user_id: int):
        return (
            db.query(PermissionDB.name)
            .join(RolePermissionDB)
            .join(RoleDB)
            .join(UserRoleDB)
            .filter(UserRoleDB.user_id == user_id)
            .all()
        )

    def get_role_by_name(self, db, name):
        return db.query(RoleDB).filter(RoleDB.name == name).first()

    def get_permission_by_name(self, db, name):
        return db.query(PermissionDB).filter(PermissionDB.name == name).first()

    def assign_role_to_user(self, db, user_id, role_id):
        obj = UserRoleDB(user_id=user_id, role_id=role_id)

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    def user_has_role(self, db, user_id, role_id):
        return (
            db.query(UserRoleDB)
            .filter(UserRoleDB.user_id == user_id, UserRoleDB.role_id == role_id)
            .first()
        )

    def assign_permission_to_role(self, db, role_id, permission_id):
        obj = RolePermissionDB(role_id=role_id, permission_id=permission_id)

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj
