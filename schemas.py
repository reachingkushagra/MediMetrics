from pydantic import BaseModel, EmailStr
from datetime import date


class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    phone: str
    email: EmailStr
    address: str
    registration_date: date


class PatientUpdate(BaseModel):
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    phone: str
    email: EmailStr
    address: str
    registration_date: date


class PatientResponse(BaseModel):
    patient_id: int
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    phone: str
    email: EmailStr
    address: str
    registration_date: date