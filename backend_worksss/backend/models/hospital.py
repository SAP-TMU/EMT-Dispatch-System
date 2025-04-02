from sqlalchemy import Column, Integer, String, Float, Enum
from db.database import Base
from models.hospital_status import HospitalStatus

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    max_beds = Column(Integer, nullable=False)  # 🆕 Added field
    available_beds = Column(Integer, nullable=False)
    status = Column(Enum(HospitalStatus), nullable=False)
