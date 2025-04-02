import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app
from db.database import SessionLocal
from sqlalchemy import text

client = TestClient(app)

# ===============================
# 🧹 Cleanup helper
# ===============================
def clean_test_data(db):
    db.execute(text("DELETE FROM reservations"))
    db.execute(text("DELETE FROM requests"))
    db.execute(text("DELETE FROM ambulances"))
    db.execute(text("DELETE FROM hospitals"))
    db.commit()

# ===============================
# 🧪 Clean DB before/after every test
# ===============================
import pytest

@pytest.fixture(autouse=True)
def clear_data():
    db = SessionLocal()
    try:
        clean_test_data(db)
        yield
        clean_test_data(db)
    finally:
        db.close()

# ===============================
# ✅ Test 1: Root Endpoint
# ===============================
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "EMS Dispatcher Backend is running."}

# ===============================
# ✅ Test 2: Add Ambulance
# ===============================
def test_create_ambulance():
    response = client.post("/ambulance/", json={
        "emt_unit": "EMT-001",
        "latitude": 43.64,
        "longitude": -79.38,
        "status": "available"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["emt_unit"] == "EMT-001"

# ===============================
# ✅ Test 3: Get All Ambulances
# ===============================
def test_get_ambulances():
    # Add another ambulance for variety
    client.post("/ambulance/", json={
        "emt_unit": "EMT-002",
        "latitude": 43.65,
        "longitude": -79.39,
        "status": "available"
    })

    response = client.get("/ambulance/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

# ===============================
# ✅ Test 4: Create Hospital
# ===============================
def test_create_hospital():
    response = client.post("/hospital/", json={
        "name": "Test Hospital",
        "address": "123 Main St, Toronto, ON",
        "max_beds": 10,
        "available_beds": 5,
        "status": "open"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Hospital"
    assert data["available_beds"] == 5

# ===============================
# ✅ Test 5: Update Hospital
# ===============================
def test_update_hospital():
    # First, create a hospital
    response = client.post("/hospital/", json={
        "name": "Update Hospital",
        "address": "500 Queen St, Toronto, ON",
        "max_beds": 10,
        "available_beds": 8,
        "status": "open"
    })
    hospital_id = response.json()["id"]

    # Now update it
    update = client.put(f"/hospital/{hospital_id}", json={
        "available_beds": 4,
        "status": "busy"
    })
    assert update.status_code == 200
    data = update.json()
    assert data["available_beds"] == 4
    assert data["status"] == "busy"
# ===============================
# ✅ Test 6: Create Request
# ===============================
def test_create_request():
    client.post("/ambulance/", json={
        "emt_unit": "EMT-004",
        "latitude": 43.64,
        "longitude": -79.38,
        "status": "available"
    })

    client.post("/hospital/", json={
        "name": "Responder Hospital",
        "address": "358 Victoria St, Toronto, ON",
        "max_beds": 10,
        "available_beds": 5,
        "status": "open"
    })

    response = client.post("/requests/", json={
        "address": "350 Victoria St, Toronto, ON",
        "severity": 2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["assigned_ambulance_id"] is not None
    assert data["assigned_hospital_id"] is not None

# ===============================
# ✅ Test 7: Reservation Override
# ===============================
def test_reservation_override():
    client.post("/ambulance/", json={
        "emt_unit": "EMT-007",
        "latitude": 43.64,
        "longitude": -79.38,
        "status": "available"
    })

    client.post("/hospital/", json={
        "name": "Override Hospital",
        "address": "359 Victoria St, Toronto, ON",
        "max_beds": 1,
        "available_beds": 1,
        "status": "open"
    })

    low = client.post("/requests/", json={
        "address": "351 Victoria St, Toronto, ON",
        "severity": 2
    })

    high = client.post("/requests/", json={
        "address": "352 Victoria St, Toronto, ON",
        "severity": 5
    })

    assert low.status_code == 200
    assert high.status_code == 200

# ===============================
# ✅ Test 8: Get Requests
# ===============================
def test_get_requests():
    client.post("/ambulance/", json={
        "emt_unit": "EMT-GETREQ",
        "latitude": 43.64,
        "longitude": -79.38,
        "status": "available"
    })

    client.post("/hospital/", json={
        "name": "Fetch Hospital",
        "address": "360 Victoria St, Toronto, ON",
        "max_beds": 5,
        "available_beds": 5,
        "status": "open"
    })

    client.post("/requests/", json={
        "address": "353 Victoria St, Toronto, ON",
        "severity": 3
    })

    response = client.get("/requests/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ===============================
# ✅ Test 9: Reassessment Trigger (fixed)
# ===============================
def test_reassessment_trigger():
    db = SessionLocal()

    hospital_res = client.post("/hospital/", json={
        "name": "Recheck Hospital",
        "address": "123 College St, Toronto, ON",  # ✅ Added
        "latitude": 43.6532,
        "longitude": -79.3832,
        "max_beds": 10,
        "available_beds": 10,
        "status": "open"
    })
    hospital_id = hospital_res.json()["id"]

    ambulance_res = client.post("/ambulance/", json={
        "emt_unit": "EMT-RECHECK",
        "latitude": 43.651070,
        "longitude": -79.347015,
        "status": "available"
    })
    ambulance_id = ambulance_res.json()["id"]

    request_res = client.post("/requests/", json={
        "address": "355 Victoria St, Toronto, ON",
        "severity": 4
    })
    request_id = request_res.json()["request_id"]

    assign = client.put(f"/requests/{request_id}", json={
        "assigned_hospital_id": hospital_id,
        "assigned_ambulance_id": ambulance_id,
        "status": "assigned"
    })
    assert assign.status_code == 200

    pickup = client.put(f"/requests/{request_id}", json={
        "status": "picked_up",
        "assigned_ambulance_id": ambulance_id,
        "assigned_hospital_id": hospital_id
    })
    assert pickup.status_code == 200
    assert pickup.json()["status"] == "picked_up"

    db.close()
# ===============================
# ✅ Test 10: Create EMT User
# ===============================
def test_create_emt_user():
    response = client.post("/create", json={
        "full_name": "EMT Alpha",
        "email": "emt.alpha@example.com",
        "phone_number": "1234567890",
        "password": "securepass",
        "role": "emt",
        "emt_unit_name": "EMT-A01",
        "address": "160 Kendal Ave, Toronto, ON"
    })
    assert response.status_code == 200 or response.status_code == 201

# ===============================
# ✅ Test 11: EMT Unit Filtering
# ===============================
def test_emt_unit_name_handling():
    client.post("/ambulance/", json={
        "emt_unit": "EMT-001",
        "latitude": 43.64,
        "longitude": -79.38,
        "status": "available"
    })
    client.post("/ambulance/", json={
        "emt_unit": "EMT-002",
        "latitude": 43.65,
        "longitude": -79.39,
        "status": "available"
    })

    response = client.get("/ambulance/?emt_unit=EMT-001")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    # This might return more than one if filtering is not working
    # Ideally only one match:
    assert all(amb["emt_unit"] == "EMT-001" for amb in data)
