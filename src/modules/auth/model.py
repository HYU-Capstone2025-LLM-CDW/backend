from sqlalchemy import Column, Integer, String, Boolean
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    password = Column(String)
    is_approved = Column(Boolean, default=False)
    role = Column(String, default="user")