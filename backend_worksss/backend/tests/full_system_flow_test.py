import requests
import time

API = "http://127.0.0.1:8000"

def post(path, payload):
    response = requests.post(f"{API}{path}", json=payload)
    print(f"➡️ POST {path} | Status: {response.status_code}")
    try:
        print("📦", response.json())
    except Exception:
        print("❌ Error parsing JSON")
    return response

def test_full_flow():
    # 1. Add Ambulance (uses Enum-compatible status)
    post("/ambulance/", {
        "latitude": 43.64,
        "longitude": -79.38,
        "status": "available"
    })

    # 2. Add Hospital (✅ now includes required 'status' field)
    post("/hospital/", {
        "name": "Test Hospital",
        "latitude": 43.65,
        "longitude": -79.39,
        "capacity": 10,
        "available_beds": 5,
        "status": "open"
    })

    # 3. Submit Emergency Request (severity is validated)
    post("/request/", {
        "latitude": 43.642,
        "longitude": -79.382,
        "severity": 3
    })

    # 4. Wait for simulation to kick in (ETA/reassignment)
    print("\n⏳ Waiting 10s to simulate movement...")
    time.sleep(10)

if __name__ == "__main__":
    test_full_flow()
