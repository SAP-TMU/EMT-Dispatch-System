# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    ambulance_router,
    hospital_router,
    request_router,
    routing_router,
    reservation_router,
    user_router  # ✅ Added
)
from db.database import create_db_and_tables  # ✅ Import the table creation function

# ✅ Create tables when app starts
create_db_and_tables()

app = FastAPI(
    title="EMS Dispatcher System",
    description="Real-time ambulance dispatch and hospital routing system.",
    version="1.0.0",
)

# CORS middleware (for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {"message": "EMS Dispatcher Backend is running."}

# Routers
app.include_router(ambulance_router.router, prefix="/ambulance")
app.include_router(hospital_router.router, prefix="/hospital")
app.include_router(request_router.router, prefix="/requests")
app.include_router(routing_router.router, prefix="/routing")
app.include_router(reservation_router.router, prefix="/reservation")
app.include_router(user_router.router)  # ✅ remove extra /users

