import requests

GOOGLE_API_KEY = "" # paste your key here

origin = "43.65,-79.38"
destination = "43.66,-79.39"
url = "https://maps.googleapis.com/maps/api/distancematrix/json"
params = {
    "origins": origin,
    "destinations": destination,
    "departure_time": "now",
    "key": GOOGLE_API_KEY
}

response = requests.get(url, params=params)
print("Status code:", response.status_code)
print("Full URL:", response.url)
print("Raw response:", response.text)
