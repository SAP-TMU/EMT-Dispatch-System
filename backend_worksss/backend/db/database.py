from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()  # ✅ Load .env file

DATABASE_URL = "sqlite:///./ems.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def create_db_and_tables():
    from models import ambulance, hospital, request, reservation, user  # ✅ Include all models
    Base.metadata.create_all(bind=engine)

# ✅ ADD THIS:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
