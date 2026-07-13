from models.user import UserDB
from models.role import Role
from models.user_role import UserRole

from security.password import hash_password


def create_admin(db):
    admin = db.query(UserDB).filter(UserDB.username == "admin").first()

    if admin:
        return admin

    admin = UserDB(username="admin", hashed_password=hash_password("admin1234"))

    db.add(admin)
    db.commit()
    db.refresh(admin)

    admin_role = db.query(Role).filter(Role.name == "admin").first()

    db.add(UserRole(user_id=admin.user_id, role_id=admin_role.id))

    db.commit()

    return admin
