from pydantic import BaseModel, field_validator
from typing import Optional
from models.hospital_status import HospitalStatus

class HospitalCreate(BaseModel):
    name: str
    address: str
    max_beds: int
    available_beds: int
    status: HospitalStatus = HospitalStatus.open

    @field_validator("available_beds")
    def validate_beds(cls, v, info):
        max_beds = info.data.get("max_beds", 0)
        if v > max_beds:
            raise ValueError("Available beds cannot exceed max beds.")
        return v

class HospitalUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    max_beds: Optional[int] = None
    available_beds: Optional[int] = None
    status: Optional[HospitalStatus] = None

class HospitalResponse(BaseModel):
    id: int
    name: str
    address: str
    latitude: float
    longitude: float
    max_beds: int
    available_beds: int
    status: HospitalStatus
    capacity_percentage: float

    class Config:
        from_attributes = True
