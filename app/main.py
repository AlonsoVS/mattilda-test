from fastapi import FastAPI
from app.api.main import api_router
from app.database import create_db_and_tables
from app.seed_data import seed_data


app = FastAPI(title="Mattilda API", description="School Management System API", version="1.0.0")

# Create database tables and seed data on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_data()

app.include_router(api_router)
