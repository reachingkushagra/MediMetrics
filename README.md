# MediMetrics - Smart Patient Appointment & Wait Time Analytics System

MediMetrics is a full-stack web application developed to streamline hospital operations by managing patients, doctors, departments, and appointments while providing insightful analytics through an interactive dashboard.

The project is built using **React**, **FastAPI**, **SQLite**, and **Pandas**, enabling hospitals to efficiently manage daily operations and gain data-driven insights into patient flow, doctor workload, and appointment trends.

---

# Features

## Patient Management

- Add new patients
- View all patients
- Update patient information
- Delete patient records
- Search patients

---

## Doctor Management

- Add new doctors
- View doctor profiles
- Update doctor details
- Delete doctors
- Search doctors

---

## Department Management

- Add hospital departments
- View department details
- Update department information
- Delete departments
- Search departments

---

## Appointment Management

- Schedule appointments
- View appointments
- Update appointment details
- Cancel/Delete appointments
- Track appointment status
- Search appointments

---

## Analytics Dashboard

Hospital insights generated using **Pandas** include:

- Total Patients
- Total Doctors
- Total Departments
- Total Appointments
- Average Patient Wait Time
- Average Consultation Time
- Peak Appointment Hours
- Doctor Workload Analysis
- Department-wise Appointment Distribution
- Appointment Status Summary
- Interactive Pie Charts

---

# Tech Stack

## Frontend

- React.js
- React Router
- Axios
- Tailwind CSS
- Chart.js
- React ChartJS 2

## Backend

- FastAPI
- Python
- Pydantic

## Database

- SQLite

## Data Analytics

- Pandas

---

# Project Structure

```text
MediMetrics/

│
├── backend/
│   ├── app.py
│   ├── analytics.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   ├── hospital.db
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── hooks/
│   ├── assets/
│   └── App.js
│
└── README.md
```

---

# Database Design

The project consists of four main tables:

### Patients

Stores patient information including personal and contact details.

### Doctors

Stores doctor information including specialization and department.

### Departments

Stores hospital departments and their locations.

### Appointments

Stores patient appointments, appointment status, consultation times, and notes.

Relationships:

```text
Department
      │
      └────────► Doctor
                     │
Patient ─────────────┤
                     │
                     └────────► Appointment
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/reachingkushagra/MediMetrics.git

cd MediMetrics
```

---

# Backend Setup

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the FastAPI server

```bash
python -m uvicorn app:app --reload
```

API Documentation

```text
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

Navigate to the frontend directory

```bash
cd frontend
```

Install dependencies

```bash
npm install
```

Start the React application

```bash
npm start
```

Frontend

```text
http://localhost:3000
```

---

# API Endpoints

## Patients

| Method | Endpoint |
|---------|----------|
| GET | /patients |
| GET | /patients/{id} |
| POST | /patients |
| PUT | /patients/{id} |
| DELETE | /patients/{id} |

---

## Doctors

| Method | Endpoint |
|---------|----------|
| GET | /doctors |
| GET | /doctors/{id} |
| POST | /doctors |
| PUT | /doctors/{id} |
| DELETE | /doctors/{id} |

---

## Departments

| Method | Endpoint |
|---------|----------|
| GET | /departments |
| GET | /departments/{id} |
| POST | /departments |
| PUT | /departments/{id} |
| DELETE | /departments/{id} |

---

## Appointments

| Method | Endpoint |
|---------|----------|
| GET | /appointments |
| GET | /appointments/{id} |
| POST | /appointments |
| PUT | /appointments/{id} |
| DELETE | /appointments/{id} |

---

## Analytics

| Method | Endpoint |
|---------|----------|
| GET | /analytics |

---

# Dashboard Metrics

The analytics dashboard provides:

- Total Patients
- Total Doctors
- Total Departments
- Total Appointments
- Average Wait Time
- Average Consultation Time
- Peak Appointment Hour
- Doctor Workload
- Department-wise Appointments
- Appointment Status Distribution

---

# Screenshots

## Dashboard


---

## Patients Module


---

## Doctors Module


---

## Departments Module


---

## Appointments Module


---

# Validation

- CRUD operations implemented for Patients, Doctors, Departments, and Appointments.
- Input validation using Pydantic schemas.
- Proper HTTP status codes and exception handling.
- SQLite foreign key relationships maintain data integrity.
- Analytics generated from live database records using Pandas.
- Responsive React frontend integrated with FastAPI backend.

---

# Author

**Kushagra Verma**

GitHub: https://github.com/reachingkushagra

LinkedIn: https://www.linkedin.com/in/reachingkushagra/

---

# License

This project is developed for educational and learning purposes.