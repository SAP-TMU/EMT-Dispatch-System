from pydantic import BaseModel, model_validator
from typing import Optional
from models.request_status import RequestStatus

class RequestCreate(BaseModel):
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    severity: int

    @model_validator(mode="after")
    def check_coordinates_or_address(self) -> 'RequestCreate':
        if not self.address and (self.latitude is None or self.longitude is None):
            raise ValueError("Must provide either an address or both latitude and longitude.")
        return self

class RequestUpdate(BaseModel):
    status: Optional[RequestStatus] = None
    assigned_ambulance_id: Optional[int] = None
    assigned_hospital_id: Optional[int] = None

class RequestAssignmentResponse(BaseModel):
    request_id: int
    assigned_ambulance_id: Optional[int]
    assigned_hospital_id: Optional[int]
    ambulance_eta_seconds: Optional[int]
    hospital_eta_seconds: Optional[int]
    status: RequestStatus
