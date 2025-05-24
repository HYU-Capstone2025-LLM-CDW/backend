from sqlalchemy import Column, Integer, String, Boolean
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    employee_number = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    status = Column(String, default="PENDING")
    role = Column(String, default="user")
    account_locked = Column(Boolean, default=False)