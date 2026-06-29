from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sqlite_file_name = "database.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{sqlite_file_name}"

# Connect to the DB
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
    )

# Operation Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Model
class Base(DeclarativeBase):
    pass    

# dependency to give a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
