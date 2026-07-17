from fastapi import FastAPI
from models import create_tables

app = FastAPI(
    title="MediMetrics API",
    description="Smart Patient Appointment & Wait Time Analytics API",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def home():
    return {
        "message": "Welcome to MediMetrics API",
        "status": "API is running successfully!"
    }