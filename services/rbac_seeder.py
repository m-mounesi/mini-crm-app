from models.role import Role
from models.permission import Permission


class RBACSeeder:
    def seed_roles(self, db):
        roles = ["admin", "operator", "viewer"]

        for r in roles:
            exists = db.query(Role).filter(Role.name == r).first()
            if not exists:
                db.add(Role(name=r))

        db.commit()

    def seed_permissions(self, db):
        permissions = [
            # customer
            "customer.create",
            "customer.read",
            "customer.update",
            "customer.delete",
            # project
            "project.create",
            "project.read",
            "project.update",
            "project.delete",
            # task
            "task.create",
            "task.read",
            "task.update",
            "task.delete",
            # user
            "user.manage",
        ]

        for p in permissions:
            exists = db.query(Permission).filter(Permission.name == p).first()
            if not exists:
                db.add(Permission(name=p))

        db.commit()
