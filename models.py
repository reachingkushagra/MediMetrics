"""This file creates all the required database tables for the project."""

from db import get_connection


def create_tables() -> None:
    """Create the database tables if they do not already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS department (
        department_id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT NOT NULL,
        location TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctor (
        doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        specialization TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        department_id INTEGER,
        FOREIGN KEY(department_id)
        REFERENCES department(department_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patient (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender TEXT,
        date_of_birth DATE,
        phone TEXT,
        email TEXT,
        address TEXT,
        registration_date DATE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointment_status (
        status_id INTEGER PRIMARY KEY AUTOINCREMENT,
        status_name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointment (
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        status_id INTEGER NOT NULL,
        appointment_date DATE,
        appointment_time TIME,
        check_in_time TIME,
        consultation_end_time TIME,
        symptoms TEXT,
        notes TEXT,

        FOREIGN KEY(patient_id)
            REFERENCES patient(patient_id),

        FOREIGN KEY(doctor_id)
            REFERENCES doctor(doctor_id),

        FOREIGN KEY(status_id)
            REFERENCES appointment_status(status_id)
    )
    """)

    conn.commit()
    conn.close()

    print("All the tables created successfully!")
