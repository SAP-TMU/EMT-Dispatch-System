from sqlalchemy import Column, Integer, String, Float
from db.database import Base

class Ambulance(Base):
    __tablename__ = "ambulances"

    id = Column(Integer, primary_key=True, index=True)

    # Current GPS coordinates of the ambulance
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Permanent home base coordinates
    base_latitude = Column(Float, nullable=True)
    base_longitude = Column(Float, nullable=True)

    # EMT unit name (added for EMT user binding)
    emt_unit = Column(String, unique=True, nullable=True)

    # Status of the ambulance
    # Can be: available, en_route_to_patient, with_patient, returning, unavailable, offline
    status = Column(String, default="available")

    # ID of the current request assigned, if any
    current_request_id = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Ambulance(id={self.id}, status='{self.status}', lat={self.latitude}, lon={self.longitude})>"
