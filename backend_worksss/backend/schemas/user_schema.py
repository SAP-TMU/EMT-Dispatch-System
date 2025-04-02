from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from models.user import UserRole

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    role: UserRole

class UserCreate(UserBase):
    password: str
    emt_unit_name: Optional[str] = None
    address: Optional[str] = None

    @field_validator("emt_unit_name")
    def validate_emt_unit_name(cls, v, info):
        if not v:
            return v

        role = info.data.get("role")
        if role == UserRole.emt:
            if not v.startswith("EMT-") or len(v) < 5:
                raise ValueError("Invalid EMT unit name. Must start with 'EMT-' and be at least 5 characters.")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone_number: str
    role: UserRole
    emt_unit_name: Optional[str] = None

    class Config:
        from_attributes = True
