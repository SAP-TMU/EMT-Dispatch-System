from sqlalchemy import Column, Integer, ForeignKey, DateTime
from db.database import Base
from datetime import datetime

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    priority = Column(Integer, nullable=False)
    reserved_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (
            f"<Reservation(id={self.id}, request_id={self.request_id}, "
            f"hospital_id={self.hospital_id}, priority={self.priority}, "
            f"reserved_at={self.reserved_at})>"
        )
