from pydantic import BaseModel
from typing import Optional, List
from models.ambulance_status import AmbulanceStatus
from models.ambulance import Ambulance

class AmbulanceCreate(BaseModel):
    emt_unit: Optional[str] = None
    latitude: float
    longitude: float
    status: AmbulanceStatus

class AmbulanceUpdate(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: Optional[AmbulanceStatus] = None

# Pydantic model for Ambulance
class AmbulanceBase(BaseModel):
    emt_unit: Optional[str] = None
    latitude: float
    longitude: float
    status: AmbulanceStatus

    class Config:
        # Pydantic V2: Consider using `from_attributes` instead of `orm_mode`
        from_attributes = True  # Treat SQLAlchemy models like dictionaries

class AmbulanceSelfView(BaseModel):
    ambulance: Optional[AmbulanceBase] = None  # EMT's own ambulance data (if found)
    all_ambulances: List[AmbulanceBase] = []   # All ambulances in system if no EMT match

    class Config:
        from_attributes = True  # Treat SQLAlchemy models like dictionaries
