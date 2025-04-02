from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import User, UserRole
from models.ambulance import Ambulance
from schemas.user_schema import UserCreate, UserResponse
import re
from utils.google_maps import get_lat_lon_from_address

router = APIRouter()

@router.post("/create", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check for duplicate email
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.")

    # Handle EMT role and EMT unit name validation
    emt_unit_upper = user.emt_unit_name.upper() if user.emt_unit_name else None

    # Ensure EMT users have a unit name
    if user.role == UserRole.emt:
        if not emt_unit_upper:
            raise HTTPException(status_code=400, detail="EMT unit name is required for EMT role.")
        
        if not re.match(r"^EMT-[A-Z0-9]+$", emt_unit_upper):
            raise HTTPException(status_code=400, detail="EMT unit must follow format EMT-XXX.")
        
        # Only geocode and create ambulance if address is provided
        if user.address:
            lat, lon = get_lat_lon_from_address(user.address)
            if lat is None or lon is None:
                raise HTTPException(status_code=400, detail="Could not locate address.")
            
            # Create ambulance for EMT
            ambulance = Ambulance(
                emt_unit=emt_unit_upper,
                latitude=lat,
                longitude=lon,
                status="available"
            )
            db.add(ambulance)

    # Create User
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone_number=user.phone_number,
        password=user.password,  # You should hash the password here for security
        role=user.role,
        emt_unit_name=emt_unit_upper if user.role == UserRole.emt else None,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
