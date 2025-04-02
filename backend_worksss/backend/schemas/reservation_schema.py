from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReservationCreate(BaseModel):
    request_id: int
    hospital_id: int
    priority: int

class ReservationOut(BaseModel):
    id: int
    request_id: int
    hospital_id: int
    priority: int
    reserved_at: datetime

    class Config:
        from_attributes = True  # ✅ Updated for Pydantic v2
