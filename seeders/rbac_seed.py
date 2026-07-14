from sqlalchemy.orm import Session

from models.role import RoleDB
from models.permission import PermissionDB
from models.role_permission import RolePermissionDB


ROLES = ["admin", "operator", "viewer"]


PERMISSIONS = [
    # Customer
    "customer.create",
    "customer.read",
    "customer.update",
    "customer.delete",
    # Project
    "project.create",
    "project.read",
    "project.update",
    "project.delete",
    # Task
    "task.create",
    "task.read",
    "task.update",
    "task.delete",
    # User Management
    "user.manage",
]


def seed_roles(db: Session):
    for role_name in ROLES:
        exists = db.query(RoleDB).filter(RoleDB.name == role_name).first()

        if not exists:
            db.add(RoleDB(name=role_name))

    db.commit()


def seed_permissions(db: Session):
    for permission_name in PERMISSIONS:
        exists = (
            db.query(PermissionDB).filter(PermissionDB.name == permission_name).first()
        )

        if not exists:
            db.add(PermissionDB(name=permission_name))

    db.commit()

    # Connect admin permissions


def assign_admin_permissions(db):
    admin = db.query(RoleDB).filter(RoleDB.name == "admin").first()

    permissions = db.query(PermissionDB).all()

    for permission in permissions:
        exists = (
            db.query(RolePermissionDB)
            .filter(
                RolePermissionDB.role_id == admin.id,
                RolePermissionDB.permission_id == permission.id,
            )
            .first()
        )

    if not exists:
        db.add(RolePermissionDB(role_id=admin.id, permission_id=permission.id))

    db.commit()
