from fastapi import FastAPI, HTTPException
from models import create_tables
from db import get_connection
from schemas import PatientCreate
from schemas import DepartmentCreate, DepartmentUpdate
from schemas import DoctorCreate, DoctorUpdate


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