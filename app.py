from fastapi import FastAPI, HTTPException
from models import create_tables
from db import get_connection
from schemas import PatientCreate
from schemas import DepartmentCreate, DepartmentUpdate
from schemas import DoctorCreate, DoctorUpdate
from schemas import AppointmentCreate, AppointmentUpdate
import pandas as pd


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
@app.get("/patients")
def get_patients():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM patient
        """
    )

    patients = cursor.fetchall()

    conn.close()

    return patients

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM patient
        WHERE patient_id = ?
        """,
        (patient_id,)
    )

    patient = cursor.fetchone()

    conn.close()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient

@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient: PatientCreate):

    conn = get_connection()
    cursor = conn.cursor()

    # Check if patient exists
    cursor.execute(
        """
        SELECT *
        FROM patient
        WHERE patient_id = ?
        """,
        (patient_id,)
    )

    existing_patient = cursor.fetchone()

    if existing_patient is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

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
            patient_id
        )
    )

    conn.commit()
    conn.close()

    return {
        "message": "Patient updated successfully",
        "patient_id": patient_id
    }
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    # Check if patient exists
    cursor.execute(
        """
        SELECT *
        FROM patient
        WHERE patient_id = ?
        """,
        (patient_id,)
    )

    patient = cursor.fetchone()

    if patient is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Delete the patient
    cursor.execute(
        """
        DELETE FROM patient
        WHERE patient_id = ?
        """,
        (patient_id,)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Patient deleted successfully",
        "patient_id": patient_id
    }

@app.post("/departments", status_code=201)
def create_department(department: DepartmentCreate):
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
def get_departments():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM department")

    departments = cursor.fetchall()

    conn.close()

    return departments

@app.get("/departments/{department_id}")
def get_department(department_id: int):
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

    return department

@app.put("/departments/{department_id}")
def update_department(
    department_id: int,
    department: DepartmentUpdate,
):
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
def delete_department(department_id: int):
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
def create_doctor(doctor: DoctorCreate):
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

    return {
        "message": "Doctor created successfully",
        "doctor_id": doctor_id
    }


@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
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
def update_doctor(doctor_id: int, doctor: DoctorUpdate):
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
def get_doctor(doctor_id: int):
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

    return doctor

@app.get("/doctors")
def get_doctors():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM doctor")

    doctors = cursor.fetchall()

    conn.close()

    return doctors


@app.post("/appointments", status_code=201)
def create_appointment(appointment: AppointmentCreate):
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
            appointment.check_in_time.isoformat() if appointment.check_in_time else None,
            appointment.consultation_end_time.isoformat() if appointment.consultation_end_time else None,
            appointment.symptoms,
            appointment.notes,
        )
    )

    conn.commit()
    appointment_id = cursor.lastrowid
    conn.close()

    return {
        "message": "Appointment created successfully",
        "appointment_id": appointment_id
    }

@app.get("/appointments")
def get_appointments():
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

    appointments = cursor.fetchall()
    conn.close()

    return appointments

@app.get("/appointments/{appointment_id}")
def get_appointment(appointment_id: int):
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
        (appointment_id,)
    )

    appointment = cursor.fetchone()
    conn.close()

    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return appointment

@app.put("/appointments/{appointment_id}")
def update_appointment(appointment_id: int, appointment: AppointmentUpdate):
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
            appointment.check_in_time.isoformat() if appointment.check_in_time else None,
            appointment.consultation_end_time.isoformat() if appointment.consultation_end_time else None,
            appointment.symptoms,
            appointment.notes,
            appointment_id,
        )
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Appointment not found")

    conn.close()

    return {"message": "Appointment updated successfully"}


@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM appointment WHERE appointment_id = ?",
        (appointment_id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Appointment not found")

    conn.close()

    return {"message": "Appointment deleted successfully"}

@app.get("/analytics/average-wait-time")
def average_wait_time():

    conn = get_connection()

    query = """
    SELECT appointment_time, check_in_time
    FROM appointment
    WHERE check_in_time IS NOT NULL
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    if df.empty:
        return {"average_wait_time_minutes": 0}

    df["appointment_time"] = pd.to_datetime(df["appointment_time"])
    df["check_in_time"] = pd.to_datetime(df["check_in_time"])

    df["wait_time"] = (
        df["check_in_time"] - df["appointment_time"]
    ).dt.total_seconds() / 60

    return {
        "average_wait_time_minutes": round(df["wait_time"].mean(), 2)
    }

@app.get("/analytics/average-consultation-time")
def average_consultation_time():

    conn = get_connection()

    query = """
    SELECT check_in_time, consultation_end_time
    FROM appointment
    WHERE check_in_time IS NOT NULL
    AND consultation_end_time IS NOT NULL
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    if df.empty:
        return {"average_consultation_minutes": 0}

    df["check_in_time"] = pd.to_datetime(df["check_in_time"])
    df["consultation_end_time"] = pd.to_datetime(df["consultation_end_time"])

    df["consultation_time"] = (
        df["consultation_end_time"] - df["check_in_time"]
    ).dt.total_seconds() / 60

    return {
        "average_consultation_minutes": round(df["consultation_time"].mean(), 2)
    }

@app.get("/analytics/doctor-workload")
def doctor_workload():

    conn = get_connection()

    query = """
    SELECT
        d.first_name || ' ' || d.last_name AS doctor,
        COUNT(a.appointment_id) AS total_appointments
    FROM doctor d
    LEFT JOIN appointment a
    ON d.doctor_id = a.doctor_id
    GROUP BY d.doctor_id
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df.to_dict(orient="records")