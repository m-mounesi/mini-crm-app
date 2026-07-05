from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base


class UserDB(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    created_at = mapped_column(DateTime, server_default=func.now(), index=True)
    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
