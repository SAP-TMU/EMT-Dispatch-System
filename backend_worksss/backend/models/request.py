# models/request.py

from sqlalchemy import Column, Integer, Float, String, Enum
from db.database import Base
from models.request_status import RequestStatus

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)  # <-- ADD THIS LINE
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    severity = Column(Integer, nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.pending, nullable=False)
    assigned_ambulance_id = Column(Integer, nullable=True)
    assigned_hospital_id = Column(Integer, nullable=True)
    ambulance_eta = Column(Integer, nullable=True)
    hospital_eta = Column(Integer, nullable=True)

    def __repr__(self):
        return (f"<Request(id={self.id}, severity={self.severity}, "
                f"status='{self.status.value}', location=({self.latitude}, {self.longitude}))>")
