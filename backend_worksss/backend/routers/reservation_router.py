# routers/reservation_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.reservation import Reservation
from models.hospital import Hospital
from models.request import Request
from schemas.reservation_schema import ReservationCreate, ReservationOut
from datetime import datetime, timezone

router = APIRouter()

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📋 Get all reservations
@router.get("/", response_model=list[ReservationOut])
def get_all_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()

# ➕ Manually create a reservation
@router.post("/", response_model=ReservationOut)
def create_reservation(data: ReservationCreate, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.id == data.hospital_id).first()
    if not hospital or hospital.available_beds <= 0:
        raise HTTPException(status_code=400, detail="Hospital unavailable or full")

    req = db.query(Request).filter(Request.id == data.request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    # Update bed count
    hospital.available_beds -= 1

    reservation = Reservation(
        request_id=data.request_id,
        hospital_id=data.hospital_id,
        priority=data.priority,
        reserved_at=datetime.now(timezone.utc)
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation

# ❌ Delete reservation
@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    res = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Reservation not found")

    hospital = db.query(Hospital).filter(Hospital.id == res.hospital_id).first()
    if hospital:
        hospital.available_beds += 1

    db.delete(res)
    db.commit()
    return {"detail": "Reservation deleted"}
