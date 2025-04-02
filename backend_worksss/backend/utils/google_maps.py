import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_lat_lon_from_address(address: str):
    if not GOOGLE_MAPS_API_KEY:
        raise Exception("Google Maps API key not found in .env")

    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        return None, None

    results = response.json().get("results")
    if not results:
        return None, None

    location = results[0]["geometry"]["location"]
    return location["lat"], location["lng"]
