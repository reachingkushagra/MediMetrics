import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: { 'Content-Type': 'application/json' },
});

const normalizeRows = (rows, keys) => rows.map((row) => {
  if (Array.isArray(row)) {
    return keys.reduce((acc, key, index) => ({ ...acc, [key]: row[index] }), {});
  }
  return row;
});

const normalizeSingle = (row, keys) => {
  if (!row) return row;
  if (Array.isArray(row)) {
    return keys.reduce((acc, key, index) => ({ ...acc, [key]: row[index] }), {});
  }
  return row;
};

export const getDashboardStats = () => api.get('/analytics/dashboard');
export const getAverageWaitTime = () => api.get('/analytics/average-wait-time');
export const getAverageConsultationTime = () => api.get('/analytics/average-consultation-time');
export const getDoctorWorkload = () => api.get('/analytics/doctor-workload');
export const getDepartmentAppointments = () => api.get('/analytics/department-appointments');
export const getPeakHours = () => api.get('/analytics/peak-hours');
export const getAppointmentStatus = () => api.get('/analytics/appointment-status');

export const getPatients = async () => {
  const response = await api.get('/patients');
  return { ...response, data: normalizeRows(response.data, ['patient_id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'phone', 'email', 'address', 'registration_date']) };
};
export const getPatient = async (id) => {
  const response = await api.get(`/patients/${id}`);
  return { ...response, data: normalizeSingle(response.data, ['patient_id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'phone', 'email', 'address', 'registration_date']) };
};
export const createPatient = (payload) => api.post('/patients', payload);
export const updatePatient = (id, payload) => api.put(`/patients/${id}`, payload);
export const deletePatient = (id) => api.delete(`/patients/${id}`);

export const getDoctors = async () => {
  const response = await api.get('/doctors');
  return { ...response, data: normalizeRows(response.data, ['doctor_id', 'first_name', 'last_name', 'specialization', 'phone', 'email', 'department_id']) };
};
export const getDoctor = async (id) => {
  const response = await api.get(`/doctors/${id}`);
  return { ...response, data: normalizeSingle(response.data, ['doctor_id', 'first_name', 'last_name', 'specialization', 'phone', 'email', 'department_id']) };
};
export const createDoctor = (payload) => api.post('/doctors', payload);
export const updateDoctor = (id, payload) => api.put(`/doctors/${id}`, payload);
export const deleteDoctor = (id) => api.delete(`/doctors/${id}`);

export const getDepartments = async () => {
  const response = await api.get('/departments');
  return { ...response, data: normalizeRows(response.data, ['department_id', 'department_name', 'location']) };
};
export const getDepartment = async (id) => {
  const response = await api.get(`/departments/${id}`);
  return { ...response, data: normalizeSingle(response.data, ['department_id', 'department_name', 'location']) };
};
export const createDepartment = (payload) => api.post('/departments', payload);
export const updateDepartment = (id, payload) => api.put(`/departments/${id}`, payload);
export const deleteDepartment = (id) => api.delete(`/departments/${id}`);

export const getAppointments = async () => {
  const response = await api.get('/appointments');
  return { ...response, data: normalizeRows(response.data, ['appointment_id', 'patient_id', 'doctor_id', 'status_id', 'appointment_date', 'appointment_time', 'check_in_time', 'consultation_end_time', 'symptoms', 'notes']) };
};
export const getAppointment = async (id) => {
  const response = await api.get(`/appointments/${id}`);
  return { ...response, data: normalizeSingle(response.data, ['appointment_id', 'patient_id', 'doctor_id', 'status_id', 'appointment_date', 'appointment_time', 'check_in_time', 'consultation_end_time', 'symptoms', 'notes']) };
};
export const createAppointment = (payload) => api.post('/appointments', payload);
export const updateAppointment = (id, payload) => api.put(`/appointments/${id}`, payload);
export const deleteAppointment = (id) => api.delete(`/appointments/${id}`);

export default api;
