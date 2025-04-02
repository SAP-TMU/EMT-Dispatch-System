# routers/routing_router.py

from fastapi import APIRouter, Query
from services.priority_engine import get_eta

router = APIRouter()

@router.get("/eta")
def get_eta_route(origin: str = Query(...), destination: str = Query(...)):
    print("🚨 Called /routing/eta with:", origin, destination)
    eta = get_eta(origin, destination)
    if eta == float("inf"):
        return {"error": "Could not fetch ETA from Google Maps"}
    return {"eta": eta}
