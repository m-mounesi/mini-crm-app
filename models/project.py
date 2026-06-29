from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base


class ProjectDB(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    status = Column(String, default="active")

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, server_default=func.now())