"""Main FastAPI application for the MediMetrics Hospital Management System."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import create_tables
from db import get_connection
from schemas import PatientCreate
from schemas import DepartmentCreate, DepartmentUpdate
from schemas import DoctorCreate, DoctorUpdate
from schemas import AppointmentCreate, AppointmentUpdate
from analytics import router as analytics_router

app = FastAPI(
    title="MediMetrics API",
    description="Smart Patient Appointment & Wait Time Analytics API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analytics_router)


@app.on_event("startup")
def startup() -> None:
    """This function creates all the database tables when the application starts."""
    create_tables()


@app.get("/")
def home() -> dict:
    """Display a welcome message for the MediMetrics API."""
    return {
        "message": "Welcome to MediMetrics API",
        "status": "API is running successfully!",
    }


@app.post("/patients", status_code=201)
def create_patient(patient: PatientCreate) -> dict:
    """Add a new patient to the hospital database."""
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

    return {"message": "Patient created successfully", "patient_id": patient_id}


@app.get("/patients")
def get_patients() -> list:
    """Get the details of all registered patients."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM patient
        """)

    patients = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return patients


@app.get("/patients/{patient_id}")
def get_patient(patient_id: int) -> dict:
    """Get the details of a patient using the patient ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM patient
        WHERE patient_id = ?
        """,
        (patient_id,),
    )

    patient = cursor.fetchone()

    conn.close()

    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    return dict(patient)


@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient: PatientCreate) -> dict:
    """Update the information of an existing patient."""
    conn = get_connection()
    cursor = conn.cursor()

    # Check if patient exists
    cursor.execute(
        """
        SELECT *
        FROM patient
        WHERE patient_id = ?
        """,
        (patient_id,),
    )

    existing_patient = cursor.fetchone()

    if existing_patient is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Patient not found")

    # Update patient details
    cursor.execute(
        """
        UPDATE patient
        SET
            first_name = ?,
            last_name = ?,
            gender = ?,
            date_of_birth = ?,
            phone = ?,
            email = ?,
            address = ?,
            registration_date = ?
        WHERE patient_id = ?
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
            patient_id,
        ),
    )

    conn.commit()
    conn.close()

    return {"message": "Patient updated successfully", "patient_id": patient_id}


@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int) -> dict:
    """Delete a patient from the hospital database."""
    conn = get_connection()
    cursor = conn.cursor()

    # Check if patient exists
    cursor.execute(
        """
        SELECT *
        FROM patient
        WHERE patient_id = ?
        """,
        (patient_id,),
    )

    patient = cursor.fetchone()

    if patient is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Patient not found")

    # Delete the patient
    cursor.execute(
        """
        DELETE FROM patient
        WHERE patient_id = ?
        """,
        (patient_id,),
    )

    conn.commit()
    conn.close()

    return {"message": "Patient deleted successfully", "patient_id": patient_id}


@app.post("/departments", status_code=201)
def create_department(department: DepartmentCreate) -> dict:
    """Create a new department in the hospital."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO department (department_name, location)
        VALUES (?, ?)
        """,
        (
            department.department_name,
            department.location,
        ),
    )

    conn.commit()

    department_id = cursor.lastrowid

    conn.close()

    return {
        "message": "Department created successfully",
        "department_id": department_id,
    }


@app.get("/departments")
def get_departments() -> list:
    """Get the details of all departments."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM department")

    departments = [dict(row) for row in cursor.fetchall()]

    return departments


@app.get("/departments/{department_id}")
def get_department(department_id: int) -> dict:
    """Get the details of a department using the department ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM department WHERE department_id = ?",
        (department_id,),
    )

    department = cursor.fetchone()

    conn.close()

    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    return dict(department)


@app.put("/departments/{department_id}")
def update_department(
    department_id: int,
    department: DepartmentUpdate,
) -> dict:
    """Update the details of a department."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE department
        SET
            department_name = ?,
            location = ?
        WHERE department_id = ?
        """,
        (
            department.department_name,
            department.location,
            department_id,
        ),
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Department not found")

    conn.close()

    return {"message": "Department updated successfully"}


@app.delete("/departments/{department_id}")
def delete_department(department_id: int) -> dict:
    """Cancel or delete an appointment."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM department WHERE department_id = ?",
        (department_id,),
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Department not found")

    conn.close()

    return {"message": "Department deleted successfully"}


@app.post("/doctors", status_code=201)
def create_doctor(doctor: DoctorCreate) -> dict:
    """Add a new doctor to the hospital."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO doctor
        (
            first_name,
            last_name,
            specialization,
            phone,
            email,
            department_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            doctor.first_name,
            doctor.last_name,
            doctor.specialization,
            doctor.phone,
            doctor.email,
            doctor.department_id,
        ),
    )

    conn.commit()

    doctor_id = cursor.lastrowid

    conn.close()

    return {"message": "Doctor created successfully", "doctor_id": doctor_id}


@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int) -> dict:
    """Delete a doctor from the hospital database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM doctor WHERE doctor_id = ?",
        (doctor_id,),
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Doctor not found")

    conn.close()

    return {"message": "Doctor deleted successfully"}


@app.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, doctor: DoctorUpdate) -> dict:
    """Update the details of a doctor."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE doctor
        SET
            first_name = ?,
            last_name = ?,
            specialization = ?,
            phone = ?,
            email = ?,
            department_id = ?
        WHERE doctor_id = ?
        """,
        (
            doctor.first_name,
            doctor.last_name,
            doctor.specialization,
            doctor.phone,
            doctor.email,
            doctor.department_id,
            doctor_id,
        ),
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Doctor not found")

    conn.close()

    return {"message": "Doctor updated successfully"}


@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int) -> dict:
    """Get the details of a doctor using the doctor ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM doctor WHERE doctor_id = ?",
        (doctor_id,),
    )

    doctor = cursor.fetchone()

    conn.close()

    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return dict(doctor)


@app.get("/doctors")
def get_doctors() -> list:
    """Get the details of all doctors in the hospital."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM doctor")

    doctors = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return doctors


@app.post("/appointments", status_code=201)
def create_appointment(appointment: AppointmentCreate) -> dict:
    """Book a new appointment for a patient."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO appointment
        (
            patient_id,
            doctor_id,
            status_id,
            appointment_date,
            appointment_time,
            check_in_time,
            consultation_end_time,
            symptoms,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            appointment.patient_id,
            appointment.doctor_id,
            appointment.status_id,
            appointment.appointment_date.isoformat(),
            appointment.appointment_time.isoformat(),
            (
                appointment.check_in_time.isoformat()
                if appointment.check_in_time
                else None
            ),
            (
                appointment.consultation_end_time.isoformat()
                if appointment.consultation_end_time
                else None
            ),
            appointment.symptoms,
            appointment.notes,
        ),
    )

    conn.commit()
    appointment_id = cursor.lastrowid
    conn.close()

    return {
        "message": "Appointment created successfully",
        "appointment_id": appointment_id,
    }


@app.get("/appointments")
def get_appointments() -> list:
    """Get the details of all appointments."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            appointment_id,
            patient_id,
            doctor_id,
            status_id,
            appointment_date,
            appointment_time,
            check_in_time,
            consultation_end_time,
            symptoms,
            notes
        FROM appointment
    """)

    appointments = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return appointments


@app.get("/appointments/{appointment_id}")
def get_appointment(appointment_id: int) -> dict:
    """Get the details of an appointment using the appointment ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            appointment_id,
            patient_id,
            doctor_id,
            status_id,
            appointment_date,
            appointment_time,
            check_in_time,
            consultation_end_time,
            symptoms,
            notes
        FROM appointment
        WHERE appointment_id = ?
        """,
        (appointment_id,),
    )

    appointment = cursor.fetchone()
    conn.close()

    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return dict(appointment)


@app.put("/appointments/{appointment_id}")
def update_appointment(appointment_id: int, appointment: AppointmentUpdate) -> dict:
    """Update the details of an existing appointment."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE appointment
        SET
            patient_id = ?,
            doctor_id = ?,
            status_id = ?,
            appointment_date = ?,
            appointment_time = ?,
            check_in_time = ?,
            consultation_end_time = ?,
            symptoms = ?,
            notes = ?
        WHERE appointment_id = ?
        """,
        (
            appointment.patient_id,
            appointment.doctor_id,
            appointment.status_id,
            appointment.appointment_date.isoformat(),
            appointment.appointment_time.isoformat(),
            (
                appointment.check_in_time.isoformat()
                if appointment.check_in_time
                else None
            ),
            (
                appointment.consultation_end_time.isoformat()
                if appointment.consultation_end_time
                else None
            ),
            appointment.symptoms,
            appointment.notes,
            appointment_id,
        ),
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Appointment not found")

    conn.close()

    return {"message": "Appointment updated successfully"}


@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int) -> dict:
    """Cancel or delete an appointment."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM appointment WHERE appointment_id = ?", (appointment_id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Appointment not found")

    conn.close()

    return {"message": "Appointment deleted successfully"}
