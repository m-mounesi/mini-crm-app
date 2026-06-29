from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base


class NoteDB(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)

    content = Column(String, nullable=False)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, server_default=func.now())