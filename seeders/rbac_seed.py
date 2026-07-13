from sqlalchemy.orm import Session

from models.role import Role
from models.permission import Permission
from models.role_permission import RolePermission


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
        exists = db.query(Role).filter(Role.name == role_name).first()

        if not exists:
            db.add(Role(name=role_name))

    db.commit()


def seed_permissions(db: Session):
    for permission_name in PERMISSIONS:
        exists = db.query(Permission).filter(Permission.name == permission_name).first()

        if not exists:
            db.add(Permission(name=permission_name))

    db.commit()

    # Connect admin permissions


def assign_admin_permissions(db):
    admin = db.query(Role).filter(Role.name == "admin").first()

    permissions = db.query(Permission).all()

    for permission in permissions:
        exists = (
            db.query(RolePermission)
            .filter(
                RolePermission.role_id == admin.id,
                RolePermission.permission_id == permission.id,
            )
            .first()
        )

    if not exists:
        db.add(RolePermission(role_id=admin.id, permission_id=permission.id))

    db.commit()
