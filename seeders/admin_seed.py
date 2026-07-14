from models.user import UserDB
from models.role import RoleDB
from models.user_role import UserRoleDB

from security.password import hash_password


def create_admin(db):
    admin = db.query(UserDB).filter(UserDB.username == "admin").first()

    if admin:
        return admin

    admin = UserDB(username="admin", hashed_password=hash_password("admin1234"))

    db.add(admin)
    db.commit()
    db.refresh(admin)

    admin_role = db.query(RoleDB).filter(RoleDB.name == "admin").first()

    db.add(UserRoleDB(user_id=admin.user_id, role_id=admin_role.id))

    db.commit()

    return admin
