from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from core.database import Base


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True)

    role_id = Column(Integer, ForeignKey("roles.id"), index=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), index=True)

    __table_args__ = (UniqueConstraint("role_id", "permission_id"),)
