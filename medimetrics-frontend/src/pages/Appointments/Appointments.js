import React, { useEffect, useMemo, useState } from 'react';
import Button from '../../components/Button/Button';
import DataTable from '../../components/DataTable/DataTable';
import Loader from '../../components/Loader/Loader';
import Modal from '../../components/Modal/Modal';
import PageHeader from '../../components/PageHeader/PageHeader';
import SearchBar from '../../components/SearchBar/SearchBar';
import { createAppointment, deleteAppointment, getAppointments, getDoctors, getPatients, updateAppointment } from '../../services/api';

const emptyForm = {
  patient_id: '',
  doctor_id: '',
  status_id: '',
  appointment_date: '',
  appointment_time: '',
  check_in_time: '',
  consultation_end_time: '',
  symptoms: '',
  notes: '',
};

const Appointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [patients, setPatients] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [modalOpen, setModalOpen] = useState(false);
  const [editingAppointment, setEditingAppointment] = useState(null);
  const [form, setForm] = useState(emptyForm);

  const fetchAppointments = async () => {
    try {
      setLoading(true);
      const [appointmentResponse, patientResponse, doctorResponse] = await Promise.all([
        getAppointments(),
        getPatients(),
        getDoctors(),
      ]);
      setAppointments(appointmentResponse.data || []);
      setPatients(patientResponse.data || []);
      setDoctors(doctorResponse.data || []);
    } catch (err) {
      setError('Unable to load appointments.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAppointments();
  }, []);

  const filteredAppointments = useMemo(() => {
    const term = search.toLowerCase();
    return appointments.filter((appointment) => `${appointment.symptoms} ${appointment.notes}`.toLowerCase().includes(term));
  }, [appointments, search]);

  const handleOpenCreate = () => {
    setEditingAppointment(null);
    setForm(emptyForm);
    setModalOpen(true);
  };

  const handleOpenEdit = (appointment) => {
    setEditingAppointment(appointment);
    setForm({
      patient_id: appointment.patient_id || '',
      doctor_id: appointment.doctor_id || '',
      status_id: appointment.status_id || '',
      appointment_date: appointment.appointment_date || '',
      appointment_time: appointment.appointment_time || '',
      check_in_time: appointment.check_in_time || '',
      consultation_end_time: appointment.consultation_end_time || '',
      symptoms: appointment.symptoms || '',
      notes: appointment.notes || '',
    });
    setModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...form,
        patient_id: Number(form.patient_id),
        doctor_id: Number(form.doctor_id),
        status_id: Number(form.status_id),
      };
      if (editingAppointment) {
        await updateAppointment(editingAppointment.appointment_id, payload);
      } else {
        await createAppointment(payload);
      }
      setModalOpen(false);
      fetchAppointments();
    } catch (err) {
      setError('The request could not be completed.');
    }
  };

  const handleDelete = async (appointmentId) => {
    try {
      await deleteAppointment(appointmentId);
      fetchAppointments();
    } catch (err) {
      setError('Unable to delete appointment.');
    }
  };

  const patientMap = Object.fromEntries(patients.map((patient) => [patient.patient_id, `${patient.first_name} ${patient.last_name}`]));
  const doctorMap = Object.fromEntries(doctors.map((doctor) => [doctor.doctor_id, `${doctor.first_name} ${doctor.last_name}`]));
  const statusMap = {
    1: 'Scheduled',
    2: 'Completed',
    3: 'Cancelled',
    4: 'No-show',
  };

  const columns = [
    { header: 'Appointment ID', key: 'appointment_id' },
    { header: 'Patient', key: 'patient_id', render: (row) => patientMap[row.patient_id] || row.patient_id },
    { header: 'Doctor', key: 'doctor_id', render: (row) => doctorMap[row.doctor_id] || row.doctor_id },
    { header: 'Status', key: 'status_id', render: (row) => statusMap[row.status_id] || row.status_id },
    { header: 'Date', key: 'appointment_date' },
    { header: 'Time', key: 'appointment_time' },
    { header: 'Symptoms', key: 'symptoms' },
    {
      header: 'Actions',
      key: 'actions',
      render: (row) => (
        <div style={{ display: 'flex', gap: '8px' }}>
          <Button variant="outline" onClick={() => handleOpenEdit(row)}>Edit</Button>
          <Button variant="danger" onClick={() => handleDelete(row.appointment_id)}>Delete</Button>
        </div>
      ),
    },
  ];

  return (
    <div>
      <PageHeader title="Appointments" subtitle="Schedule and manage care visits" actionLabel="Add Appointment" onAction={handleOpenCreate} />
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', gap: '12px', flexWrap: 'wrap' }}>
        <SearchBar value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search appointments" />
      </div>
      {error && <div style={{ color: '#EF4444', marginBottom: '12px' }}>{error}</div>}
      {loading ? <Loader /> : <DataTable columns={columns} data={filteredAppointments} emptyMessage="No Records Found" />}

      <Modal open={modalOpen} title={editingAppointment ? 'Edit Appointment' : 'Add Appointment'} onClose={() => setModalOpen(false)}>
        <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '12px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px' }}>
            <select value={form.patient_id} onChange={(e) => setForm({ ...form, patient_id: e.target.value })} required style={fieldStyle}>
              <option value="">Select Patient</option>
              {patients.map((patient) => (
                <option key={patient.patient_id} value={patient.patient_id}>{`${patient.first_name} ${patient.last_name}`}</option>
              ))}
            </select>
            <select value={form.doctor_id} onChange={(e) => setForm({ ...form, doctor_id: e.target.value })} required style={fieldStyle}>
              <option value="">Select Doctor</option>
              {doctors.map((doctor) => (
                <option key={doctor.doctor_id} value={doctor.doctor_id}>{`${doctor.first_name} ${doctor.last_name}`}</option>
              ))}
            </select>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px' }}>
            <select value={form.status_id} onChange={(e) => setForm({ ...form, status_id: e.target.value })} required style={fieldStyle}>
              <option value="">Select Status</option>
              <option value="1">Scheduled</option>
              <option value="2">Completed</option>
              <option value="3">Cancelled</option>
              <option value="4">No-show</option>
            </select>
            <input type="date" value={form.appointment_date} onChange={(e) => setForm({ ...form, appointment_date: e.target.value })} required style={fieldStyle} />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px' }}>
            <input type="time" value={form.appointment_time} onChange={(e) => setForm({ ...form, appointment_time: e.target.value })} required style={fieldStyle} />
            <input type="time" value={form.check_in_time} onChange={(e) => setForm({ ...form, check_in_time: e.target.value })} style={fieldStyle} />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px' }}>
            <input type="time" value={form.consultation_end_time} onChange={(e) => setForm({ ...form, consultation_end_time: e.target.value })} style={fieldStyle} />
            <input value={form.symptoms} onChange={(e) => setForm({ ...form, symptoms: e.target.value })} placeholder="Symptoms" required style={fieldStyle} />
          </div>
          <textarea value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} placeholder="Notes" style={{ ...fieldStyle, minHeight: '90px' }} />
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px' }}>
            <Button variant="outline" onClick={() => setModalOpen(false)}>Cancel</Button>
            <Button type="submit">Save</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

const fieldStyle = {
  width: '100%',
  padding: '10px 12px',
  borderRadius: '10px',
  border: '1px solid #E2E8F0',
  boxSizing: 'border-box',
};

export default Appointments;
