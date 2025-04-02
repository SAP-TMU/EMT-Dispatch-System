from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.hospital import Hospital
from schemas.hospital_schema import HospitalCreate, HospitalUpdate, HospitalResponse
from utils.google_maps import get_lat_lon_from_address
from models.hospital_status import HospitalStatus
from typing import List

router = APIRouter()

# ➕ Create hospital
@router.post("/", response_model=HospitalResponse)
def create_hospital(hospital: HospitalCreate, db: Session = Depends(get_db)):
    # Convert address to coordinates
    lat, lon = get_lat_lon_from_address(hospital.address)
    if lat is None or lon is None:
        raise HTTPException(status_code=400, detail="Invalid address provided.")

    if hospital.available_beds > hospital.max_beds:
        raise HTTPException(status_code=400, detail="Available beds cannot exceed max beds.")

    status = HospitalStatus.busy if hospital.available_beds == 0 else hospital.status

    db_hospital = Hospital(
        name=hospital.name,
        address=hospital.address,
        latitude=lat,
        longitude=lon,
        max_beds=hospital.max_beds,
        available_beds=hospital.available_beds,
        status=status
    )
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)

    response = HospitalResponse(
        id=db_hospital.id,
        name=db_hospital.name,
        address=db_hospital.address,
        latitude=db_hospital.latitude,
        longitude=db_hospital.longitude,
        max_beds=db_hospital.max_beds,
        available_beds=db_hospital.available_beds,
        status=db_hospital.status,
        capacity_percentage=(db_hospital.available_beds / db_hospital.max_beds) * 100
    )
    return response

# 📝 Update hospital
@router.put("/{hospital_id}", response_model=HospitalResponse)
def update_hospital(hospital_id: int, data: HospitalUpdate, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    if data.address:
        lat, lon = get_lat_lon_from_address(data.address)
        if lat is None or lon is None:
            raise HTTPException(status_code=400, detail="Invalid address.")
        hospital.address = data.address
        hospital.latitude = lat
        hospital.longitude = lon

    if data.name:
        hospital.name = data.name
    if data.max_beds is not None:
        hospital.max_beds = data.max_beds
    if data.available_beds is not None:
        if data.max_beds is not None and data.available_beds > data.max_beds:
            raise HTTPException(status_code=400, detail="Available beds exceed max beds.")
        if data.available_beds > hospital.max_beds:
            raise HTTPException(status_code=400, detail="Available beds exceed max beds.")
        hospital.available_beds = data.available_beds
    if data.status:
        hospital.status = data.status

    # Auto-set status to busy if no beds
    if hospital.available_beds == 0:
        hospital.status = HospitalStatus.busy

    db.commit()
    db.refresh(hospital)

    return HospitalResponse(
        id=hospital.id,
        name=hospital.name,
        address=hospital.address,
        latitude=hospital.latitude,
        longitude=hospital.longitude,
        max_beds=hospital.max_beds,
        available_beds=hospital.available_beds,
        status=hospital.status,
        capacity_percentage=(hospital.available_beds / hospital.max_beds) * 100
    )

# 📄 Get all hospitals
@router.get("/", response_model=List[HospitalResponse])
def get_hospitals(db: Session = Depends(get_db)):
    hospitals = db.query(Hospital).all()
    return [
        HospitalResponse(
            id=h.id,
            name=h.name,
            address=h.address,
            latitude=h.latitude,
            longitude=h.longitude,
            max_beds=h.max_beds,
            available_beds=h.available_beds,
            status=h.status,
            capacity_percentage=(h.available_beds / h.max_beds) * 100
        ) for h in hospitals
    ]
