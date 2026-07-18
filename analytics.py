from fastapi import APIRouter
from db import get_connection
import pandas as pd

router = APIRouter(prefix="/analytics", tags=["Analytics"])
@router.get("/dashboard")
def dashboard():

    conn = get_connection()

    patients = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM patient",
        conn
    )

    doctors = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM doctor",
        conn
    )

    departments = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM department",
        conn
    )

    appointments = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM appointment",
        conn
    )

    conn.close()

    return {
        "total_patients": int(patients.iloc[0]["total"]),
        "total_doctors": int(doctors.iloc[0]["total"]),
        "total_departments": int(departments.iloc[0]["total"]),
        "total_appointments": int(appointments.iloc[0]["total"])
    }

@router.get("/average-wait-time")
def average_wait_time():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT appointment_time, check_in_time
        FROM appointment
        WHERE check_in_time IS NOT NULL
        """,
        conn,
    )

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

@router.get("/average-consultation-time")
def average_consultation_time():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT check_in_time, consultation_end_time
        FROM appointment
        WHERE check_in_time IS NOT NULL
        AND consultation_end_time IS NOT NULL
        """,
        conn,
    )

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

@router.get("/doctor-workload")
def doctor_workload():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            d.first_name || ' ' || d.last_name AS doctor,
            COUNT(a.appointment_id) AS total_appointments
        FROM doctor d
        LEFT JOIN appointment a
        ON d.doctor_id = a.doctor_id
        GROUP BY d.doctor_id
        """,
        conn,
    )

    conn.close()

    return df.to_dict(orient="records")

@router.get("/department-appointments")
def department_appointments():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            dep.department_name,
            COUNT(a.appointment_id) AS total_appointments
        FROM department dep
        LEFT JOIN doctor d
        ON dep.department_id = d.department_id
        LEFT JOIN appointment a
        ON d.doctor_id = a.doctor_id
        GROUP BY dep.department_name
        """,
        conn,
    )

    conn.close()

    return df.to_dict(orient="records")

@router.get("/peak-hours")
def peak_hours():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT appointment_time FROM appointment",
        conn,
    )

    conn.close()

    if df.empty:
        return []

    df["appointment_time"] = pd.to_datetime(df["appointment_time"])
    df["hour"] = df["appointment_time"].dt.hour

    result = (
        df.groupby("hour")
        .size()
        .reset_index(name="appointments")
    )

    return result.to_dict(orient="records")

@router.get("/appointment-status")
def appointment_status():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            s.status_name,
            COUNT(a.appointment_id) AS total
        FROM appointment_status s
        LEFT JOIN appointment a
        ON s.status_id = a.status_id
        GROUP BY s.status_name
        """,
        conn,
    )

    conn.close()

    return df.to_dict(orient="records")