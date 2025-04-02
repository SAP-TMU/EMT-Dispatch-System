from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.ambulance import Ambulance
from models.ambulance_status import AmbulanceStatus
from schemas.ambulance_schema import AmbulanceCreate, AmbulanceUpdate, AmbulanceSelfView
from typing import Optional

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🚑 Get all ambulances, optionally filtered by emt_unit
@router.get("/")
def get_ambulances(
    emt_unit: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Ambulance)
    if emt_unit:
        query = query.filter(Ambulance.emt_unit == emt_unit)
    return query.all()

# ➕ Add a new ambulance
@router.post("/")
def create_ambulance(ambulance: AmbulanceCreate, db: Session = Depends(get_db)):
    if ambulance.status not in AmbulanceStatus:
        raise HTTPException(status_code=400, detail="Invalid ambulance status")
    
    new_amb = Ambulance(
        emt_unit=ambulance.emt_unit,
        latitude=ambulance.latitude,
        longitude=ambulance.longitude,
        status=ambulance.status,
        current_request_id=None
    )
    db.add(new_amb)
    db.commit()
    db.refresh(new_amb)
    return new_amb

# 🔄 Update ambulance status/location
@router.put("/{ambulance_id}")
def update_ambulance(ambulance_id: int, data: AmbulanceUpdate, db: Session = Depends(get_db)):
    amb = db.query(Ambulance).filter(Ambulance.id == ambulance_id).first()
    if not amb:
        raise HTTPException(status_code=404, detail="Ambulance not found")

    if data.latitude is not None:
        amb.latitude = data.latitude
    if data.longitude is not None:
        amb.longitude = data.longitude
    if data.status is not None:
        if data.status not in AmbulanceStatus:
            raise HTTPException(status_code=400, detail="Invalid ambulance status")
        amb.status = data.status

    db.commit()
    db.refresh(amb)
    return amb

# 🚑 View ambulance data for a specific EMT or all ambulances if not found
@router.get("/me")
def get_ambulance_for_emts(emt_unit: Optional[str] = None, db: Session = Depends(get_db)):
    if emt_unit:
        ambulances = db.query(Ambulance).filter(Ambulance.emt_unit == emt_unit).all()
        if ambulances:
            return AmbulanceSelfView(ambulance=ambulances[0], all_ambulances=[])
        else:
            all_ambulances = db.query(Ambulance).all()
            return AmbulanceSelfView(ambulance=None, all_ambulances=all_ambulances)

    all_ambulances = db.query(Ambulance).all()
    return AmbulanceSelfView(ambulance=None, all_ambulances=all_ambulances)
