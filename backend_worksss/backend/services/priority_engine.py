from models.hospital_status import HospitalStatus  # ✅ Correct
import math, os, requests, asyncio
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from models.ambulance import Ambulance
from models.hospital import Hospital
from models.request import Request
from models.reservation import Reservation
from models.ambulance_status import AmbulanceStatus
from models.request_status import RequestStatus

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

BASE_LAT = 43.651070
BASE_LON = -79.347015

def calculate_distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)

def get_eta(origin, destination):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "key": GOOGLE_API_KEY,
        "departure_time": "now"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        element = data["rows"][0]["elements"][0]

        if element.get("status") != "OK":
            return float("inf")

        return element.get("duration_in_traffic", element.get("duration"))["value"]

    except Exception:
        return float("inf")
def assign_ambulance_and_hospital(db: Session, req: Request):
    if req.assigned_ambulance_id or req.assigned_hospital_id:
        return

    ambulances = db.query(Ambulance).filter(Ambulance.status == "available").all()
    if not ambulances:
        return

    sorted_ambs = sorted(ambulances, key=lambda amb: calculate_distance(
        amb.latitude, amb.longitude, req.latitude, req.longitude))[:3]

    amb_etas = []
    for amb in sorted_ambs:
        eta = get_eta(f"{amb.latitude},{amb.longitude}", f"{req.latitude},{req.longitude}")
        if eta != float("inf"):
            amb_etas.append((amb, eta))

    if not amb_etas:
        return

    best_amb, best_eta = sorted(amb_etas, key=lambda x: x[1])[0]

    req.assigned_ambulance_id = best_amb.id
    req.ambulance_eta = best_eta
    best_amb.status = AmbulanceStatus.en_route_to_patient

    hospitals = db.query(Hospital).filter(Hospital.available_beds > 0).all()
    if not hospitals:
        return

    sorted_hosps = sorted(hospitals, key=lambda hosp: calculate_distance(
        req.latitude, req.longitude, hosp.latitude, hosp.longitude))[:3]

    hosp_etas = []
    for hosp in sorted_hosps:
        eta = get_eta(f"{req.latitude},{req.longitude}", f"{hosp.latitude},{hosp.longitude}")
        if eta != float("inf"):
            hosp_etas.append((hosp, eta))

    if not hosp_etas:
        return

    best_hosp, hosp_eta = sorted(hosp_etas, key=lambda x: x[1])[0]
    req.assigned_hospital_id = best_hosp.id
    req.hospital_eta = hosp_eta
    best_hosp.available_beds -= 1
    if best_hosp.available_beds == 0:
        best_hosp.status = HospitalStatus.busy

    reservation = Reservation(
        request_id=req.id,
        hospital_id=best_hosp.id,
        priority=req.severity,
        reserved_at=datetime.now(timezone.utc)
    )
    db.add(reservation)
def find_best_ambulance(req: Request, db: Session):
    ambulances = db.query(Ambulance).filter(Ambulance.status == AmbulanceStatus.available).all()
    if not ambulances:
        return None, None

    top_3 = sorted(ambulances, key=lambda a: calculate_distance(
        a.latitude, a.longitude, req.latitude, req.longitude))[:3]

    best, best_eta = None, float("inf")
    for amb in top_3:
        eta = get_eta(f"{amb.latitude},{amb.longitude}", f"{req.latitude},{req.longitude}")
        if eta < best_eta:
            best, best_eta = amb, eta
    return best, best_eta

def find_best_hospital(req: Request, db: Session):
    hospitals = db.query(Hospital).filter(Hospital.available_beds > 0).all()
    if not hospitals:
        return None, None

    top_3 = sorted(hospitals, key=lambda h: calculate_distance(
        req.latitude, req.longitude, h.latitude, h.longitude))[:3]

    best, best_eta = None, float("inf")
    for h in top_3:
        eta = get_eta(f"{req.latitude},{req.longitude}", f"{h.latitude},{h.longitude}")
        if eta < best_eta:
            best, best_eta = h, eta
    return best, best_eta

def reserve_hospital_spot(request_id: int, hospital_id: int, priority: int, db: Session):
    existing = db.query(Reservation).filter(Reservation.hospital_id == hospital_id).all()
    for res in existing:
        if res.priority < priority:
            evicted_request_id = res.request_id
            db.delete(res)
            db.commit()

            evicted_request = db.query(Request).filter(Request.id == evicted_request_id).first()
            if evicted_request:
                available_hospitals = db.query(Hospital).filter(
                    Hospital.available_beds > 0,
                    Hospital.id != hospital_id
                ).all()

                top_3 = sorted(available_hospitals, key=lambda h: calculate_distance(
                    evicted_request.latitude, evicted_request.longitude, h.latitude, h.longitude))[:3]

                best_hosp, best_eta = None, float("inf")
                for h in top_3:
                    eta = get_eta(f"{evicted_request.latitude},{evicted_request.longitude}",
                                  f"{h.latitude},{h.longitude}")
                    if eta < best_eta:
                        best_hosp, best_eta = h, eta

                if best_hosp:
                    new_res = Reservation(
                        request_id=evicted_request_id,
                        hospital_id=best_hosp.id,
                        priority=evicted_request.severity,
                        reserved_at=datetime.now(timezone.utc)
                    )
                    db.add(new_res)
                    db.commit()
                    print(f"🔁 Reassigned evicted request {evicted_request_id} to hospital {best_hosp.id}")
            break

    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    hospital.available_beds = max(0, hospital.available_beds - 1)

    reservation = Reservation(
        request_id=request_id,
        hospital_id=hospital_id,
        priority=priority,
        reserved_at=datetime.now(timezone.utc)
    )
    db.add(reservation)
    db.commit()

async def start_eta_reassessment(request_id: int, db: Session):
    print(f"🔁 Starting hospital reassessment loop for request {request_id}")
    MAX_REROUTE_THRESHOLD = 600  # 10 minutes
    RECHECK_INTERVAL = 120       # 2 minutes
    ETA_IMPROVEMENT_THRESHOLD = 600  # Save 10 min

    while True:
        await asyncio.sleep(RECHECK_INTERVAL)

        req = db.query(Request).filter(Request.id == request_id).first()
        if not req:
            print("❌ Request not found.")
            break

        reservation = db.query(Reservation).filter(Reservation.request_id == request_id).first()
        if not reservation:
            print("❌ No reservation found.")
            break

        ambulance = db.query(Ambulance).filter(Ambulance.id == req.ambulance_id).first()
        current_hospital = db.query(Hospital).filter(Hospital.id == reservation.hospital_id).first()
        if not ambulance or not current_hospital:
            print("❌ Ambulance or hospital data missing.")
            break

        origin = f"{ambulance.latitude},{ambulance.longitude}"
        dest = f"{current_hospital.latitude},{current_hospital.longitude}"
        current_eta = get_eta(origin, dest)
        print(f"📍 ETA to hospital {current_hospital.id}: {current_eta} sec")

        if current_eta < MAX_REROUTE_THRESHOLD:
            print("✅ ETA under threshold. Ending reassessment.")
            break

        hospitals = db.query(Hospital).filter(Hospital.available_beds > 0).all()
        top_3 = sorted(hospitals, key=lambda h: calculate_distance(
            req.latitude, req.longitude, h.latitude, h.longitude))[:3]

        best, best_eta = None, float("inf")
        for h in top_3:
            eta = get_eta(origin, f"{h.latitude},{h.longitude}")
            print(f"⏱ ETA to hospital {h.id}: {eta} sec")
            if eta < best_eta:
                best, best_eta = h, eta

        if best and best.id != current_hospital.id and best_eta + ETA_IMPROVEMENT_THRESHOLD < current_eta:
            print(f"🚨 Rerouting to better hospital {best.id} (ETA {best_eta})")
            db.delete(reservation)
            db.commit()

            new_res = Reservation(
                request_id=request_id,
                hospital_id=best.id,
                priority=req.severity,
                reserved_at=datetime.now(timezone.utc)
            )
            db.add(new_res)
            db.commit()
        else:
            print("⚠️ No significantly better hospital found.")
