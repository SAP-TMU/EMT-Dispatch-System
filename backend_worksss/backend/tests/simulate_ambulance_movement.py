# tests/simulate_ambulance_movement.py

import time
import requests
import math

API_BASE = "http://127.0.0.1:8000"

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def move_toward(current, target, step_size=0.0001):
    lat1, lon1 = current
    lat2, lon2 = target
    dlat, dlon = lat2 - lat1, lon2 - lon1
    dist = math.hypot(dlat, dlon)
    if dist < step_size:
        return target
    scale = step_size / dist
    return lat1 + dlat * scale, lon1 + dlon * scale

def simulate():
    # Step 1: Fetch ambulances
    print("🚑 Getting ambulance list...")
    response = requests.get(f"{API_BASE}/ambulance/")
    ambulances = response.json()

    # Step 2: Move all busy ambulances with a current_request_id
    for amb in ambulances:
        if amb["status"] != "busy" or amb["current_request_id"] is None:
            continue

        amb_id = amb["id"]
        print(f"\n🔄 Simulating ambulance {amb_id}...")

        # Get hospital destination
        request = requests.get(f"{API_BASE}/request/{amb['current_request_id']}").json()
        hospital_id = request.get("assigned_hospital_id")
        if not hospital_id:
            print("❌ No hospital assigned.")
            continue

        hospital = requests.get(f"{API_BASE}/hospital/{hospital_id}").json()
        if not hospital:
            print("❌ Hospital not found.")
            continue

        current = (amb["latitude"], amb["longitude"])
        destination = (hospital["latitude"], hospital["longitude"])

        print(f"➡️ Moving ambulance from {current} to {destination}")

        # Stepwise movement
        for _ in range(100):
            new_lat, new_lon = move_toward(current, destination)
            current = (new_lat, new_lon)

            # Update ambulance location
            update = requests.put(f"{API_BASE}/ambulance/{amb_id}", json={
                "latitude": new_lat,
                "longitude": new_lon,
                "status": "busy"
            })
            print(f"📍 Updated to {new_lat:.6f}, {new_lon:.6f}")
            time.sleep(0.3)

            # Check if close enough (within 5m)
            dist = haversine_distance(new_lat, new_lon, destination[0], destination[1])
            if dist <= 5:
                print("✅ Arrived! Should auto-mark as available via backend check.")
                break

if __name__ == "__main__":
    simulate()
