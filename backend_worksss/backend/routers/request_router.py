from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.request import Request
from models.request_status import RequestStatus
from schemas.request_schema import RequestCreate, RequestAssignmentResponse, RequestUpdate
import os
from services.priority_engine import start_eta_reassessment, assign_ambulance_and_hospital
import asyncio
from utils.google_maps import get_lat_lon_from_address

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📥 Create new emergency request
@router.post("/", response_model=RequestAssignmentResponse)
def create_request(data: RequestCreate, db: Session = Depends(get_db)):
    # ✅ Get coordinates: from address or from direct lat/lon
    if data.address:
        lat, lon = get_lat_lon_from_address(data.address)
        if lat is None or lon is None:
            raise HTTPException(status_code=400, detail="Invalid address.")
    elif data.latitude is not None and data.longitude is not None:
        lat, lon = data.latitude, data.longitude
    else:
        raise HTTPException(status_code=400, detail="Provide either address or coordinates.")

    new_req = Request(
        address=data.address,
        latitude=lat,
        longitude=lon,
        severity=data.severity,
        status=RequestStatus.pending,
        assigned_ambulance_id=None,
        assigned_hospital_id=None,
    )
    db.add(new_req)
    db.commit()
    db.refresh(new_req)

    # 🚑 Auto-assign ambulance and hospital
    assign_ambulance_and_hospital(db, new_req)
    db.commit()
    db.refresh(new_req)

    return RequestAssignmentResponse(
        request_id=new_req.id,
        assigned_ambulance_id=new_req.assigned_ambulance_id,
        assigned_hospital_id=new_req.assigned_hospital_id,
        ambulance_eta_seconds=new_req.ambulance_eta,
        hospital_eta_seconds=new_req.hospital_eta,
        status=new_req.status,
    )

# 🔍 Get all requests
@router.get("/")
def get_requests(db: Session = Depends(get_db)):
    return db.query(Request).all()

# ✏️ Update request (status, assignments)
@router.put("/{request_id}")
def update_request(request_id: int, data: RequestUpdate, db: Session = Depends(get_db)):
    req = db.query(Request).filter(Request.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    if data.status:
        if data.status not in RequestStatus:
            raise HTTPException(status_code=400, detail="Invalid request status")
        req.status = data.status

        # ✅ Trigger reassessment loop after pickup
        if data.status == RequestStatus.picked_up:
            if os.getenv("ENV") != "test":
                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(start_eta_reassessment(request_id, db))
                except RuntimeError:
                    print("⚠️ Skipping reassessment: no event loop (likely running in test environment)")

    if data.assigned_ambulance_id is not None:
        req.assigned_ambulance_id = data.assigned_ambulance_id
    if data.assigned_hospital_id is not None:
        req.assigned_hospital_id = data.assigned_hospital_id

    db.commit()
    db.refresh(req)
    return req
