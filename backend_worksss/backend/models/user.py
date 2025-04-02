from sqlalchemy import Column, Integer, String, Enum
from db.database import Base
import enum

class UserRole(str, enum.Enum):
    emt = "emt"
    dispatcher = "dispatcher"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=False)
    password = Column(String, nullable=False)  # plaintext or hashed
    role = Column(Enum(UserRole), nullable=False)
    emt_unit_name = Column(String, nullable=True)  # Only needed for EMTs
