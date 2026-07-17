from fastapi import FastAPI, HTTPException
from models import create_tables
from db import get_connection
from schemas import PatientCreate

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

@app.post("/patients", status_code=201)
def create_patient(patient: PatientCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO patient
        (
            first_name,
            last_name,
            gender,
            date_of_birth,
            phone,
            email,
            address,
            registration_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            patient.first_name,
            patient.last_name,
            patient.gender,
            patient.date_of_birth,
            patient.phone,
            patient.email,
            patient.address,
            patient.registration_date,
        ),
    )

    conn.commit()

    patient_id = cursor.lastrowid

    conn.close()

    return {
        "message": "Patient created successfully",
        "patient_id": patient_id
    }