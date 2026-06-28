from sqlalchemy.orm import Mapped ,mapped_column
from sqlalchemy import Boolean
from database import Base



class UserDB(Base):
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str]= mapped_column(nullable=False)
    role: Mapped[str]= mapped_column(default="user")
    is_active: Mapped[Boolean]= mapped_column(default=True)