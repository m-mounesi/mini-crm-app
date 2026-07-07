from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from core.database import Base


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), index=True)

    __table_args__ = (UniqueConstraint("user_id", "role_id"),)
