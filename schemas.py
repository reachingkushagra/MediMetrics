"""This file contains all request and response models used in the APIs."""

from datetime import date, time
from pydantic import BaseModel, EmailStr


class PatientCreate(BaseModel):
    """Stores the details required to create a new patient."""

    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    phone: str
    email: EmailStr
    address: str
    registration_date: date


class PatientUpdate(BaseModel):
    """Stores the details required to update an existing patient."""

    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    phone: str
    email: EmailStr
    address: str
    registration_date: date


class PatientResponse(BaseModel):
    """Stores the patient information returned by the API."""

    patient_id: int
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    phone: str
    email: EmailStr
    address: str
    registration_date: date


class DepartmentCreate(BaseModel):
    """Stores the details required to create a new department."""

    department_name: str
    location: str


class DepartmentUpdate(BaseModel):
    """Stores the details required to update an existing department."""

    department_name: str
    location: str


class DepartmentResponse(BaseModel):
    """Stores the department information returned by the API."""

    department_id: int
    department_name: str
    location: str


class DoctorCreate(BaseModel):
    """Stores the details required to add a new doctor."""

    first_name: str
    last_name: str
    specialization: str
    phone: str
    email: EmailStr
    department_id: int


class DoctorUpdate(BaseModel):
    """Stores the details required to update an existing doctor."""

    first_name: str
    last_name: str
    specialization: str
    phone: str
    email: EmailStr
    department_id: int


class DoctorResponse(BaseModel):
    """Stores the doctor information returned by the API."""

    doctor_id: int
    first_name: str
    last_name: str
    specialization: str
    phone: str
    email: EmailStr
    department_id: int


class AppointmentCreate(BaseModel):
    """Stores the details required to book a new appointment."""

    patient_id: int
    doctor_id: int
    status_id: int
    appointment_date: date
    appointment_time: time
    check_in_time: time | None = None
    consultation_end_time: time | None = None
    symptoms: str
    notes: str


class AppointmentUpdate(BaseModel):
    """Stores the details required to update an existing appointment."""

    patient_id: int
    doctor_id: int
    status_id: int
    appointment_date: date
    appointment_time: time
    check_in_time: time | None = None
    consultation_end_time: time | None = None
    symptoms: str
    notes: str
