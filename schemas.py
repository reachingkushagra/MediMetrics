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


class DepartmentCreate(BaseModel):
    department_name: str
    location: str


class DepartmentUpdate(BaseModel):
    department_name: str
    location: str


class DepartmentResponse(BaseModel):
    department_id: int
    department_name: str
    location: str


class DoctorCreate(BaseModel):
    first_name: str
    last_name : str
    specialization: str
    phone: str
    email: EmailStr
    department_id: int


class DoctorUpdate(BaseModel):
    first_name: str
    last_name: str
    specialization: str
    phone: str
    email: EmailStr
    department_id: int


class DoctorResponse(BaseModel):
    doctor_id: int
    first_name: str
    last_name: str
    specialization: str
    phone: str
    email: EmailStr
    department_id: int