import React, { useEffect, useMemo, useState } from 'react';
import Button from '../../components/Button/Button';
import DataTable from '../../components/DataTable/DataTable';
import Loader from '../../components/Loader/Loader';
import Modal from '../../components/Modal/Modal';
import PageHeader from '../../components/PageHeader/PageHeader';
import SearchBar from '../../components/SearchBar/SearchBar';
import { createPatient, deletePatient, getPatients, updatePatient } from '../../services/api';

const emptyForm = {
  first_name: '',
  last_name: '',
  gender: '',
  date_of_birth: '',
  phone: '',
  email: '',
  address: '',
  registration_date: '',
};

const Patients = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [modalOpen, setModalOpen] = useState(false);
  const [editingPatient, setEditingPatient] = useState(null);
  const [form, setForm] = useState(emptyForm);

  const fetchPatients = async () => {
    try {
      setLoading(true);
      const response = await getPatients();
      setPatients(response.data || []);
    } catch (err) {
      setError('Unable to load patients.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  const filteredPatients = useMemo(() => {
    const term = search.toLowerCase();
    return patients.filter((patient) => `${patient.first_name} ${patient.last_name} ${patient.email}`.toLowerCase().includes(term));
  }, [patients, search]);

  const handleOpenCreate = () => {
    setEditingPatient(null);
    setForm(emptyForm);
    setModalOpen(true);
  };

  const handleOpenEdit = (patient) => {
    setEditingPatient(patient);
    setForm({
      first_name: patient.first_name || '',
      last_name: patient.last_name || '',
      gender: patient.gender || '',
      date_of_birth: patient.date_of_birth || '',
      phone: patient.phone || '',
      email: patient.email || '',
      address: patient.address || '',
      registration_date: patient.registration_date || '',
    });
    setModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingPatient) {
        await updatePatient(editingPatient.patient_id, form);
      } else {
        await createPatient(form);
      }
      setModalOpen(false);
      fetchPatients();
    } catch (err) {
      setError('The request could not be completed.');
    }
  };

  const handleDelete = async (patientId) => {
    try {
      await deletePatient(patientId);
      fetchPatients();
    } catch (err) {
      setError('Unable to delete patient.');
    }
  };

  const columns = [
    { header: 'Patient ID', key: 'patient_id' },
    { header: 'Name', key: 'first_name', render: (row) => `${row.first_name} ${row.last_name}` },
    { header: 'Gender', key: 'gender' },
    { header: 'Phone', key: 'phone' },
    { header: 'Email', key: 'email' },
    { header: 'Registration Date', key: 'registration_date' },
    {
      header: 'Actions',
      key: 'actions',
      render: (row) => (
        <div style={{ display: 'flex', gap: '8px' }}>
          <Button variant="outline" onClick={() => handleOpenEdit(row)}>Edit</Button>
          <Button variant="danger" onClick={() => handleDelete(row.patient_id)}>Delete</Button>
        </div>
      ),
    },
  ];

  return (
    <div>
      <PageHeader title="Patients" subtitle="Manage patient records and appointments" actionLabel="Add Patient" onAction={handleOpenCreate} />
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', gap: '12px', flexWrap: 'wrap' }}>
        <SearchBar value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search patients" />
      </div>
      {error && <div style={{ color: '#EF4444', marginBottom: '12px' }}>{error}</div>}
      {loading ? <Loader /> : <DataTable columns={columns} data={filteredPatients} emptyMessage="No Records Found" />}

      <Modal open={modalOpen} title={editingPatient ? 'Edit Patient' : 'Add Patient'} onClose={() => setModalOpen(false)}>
        <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '12px' }}>
          <input value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} placeholder="First Name" required style={fieldStyle} />
          <input value={form.last_name} onChange={(e) => setForm({ ...form, last_name: e.target.value })} placeholder="Last Name" required style={fieldStyle} />
          <input value={form.gender} onChange={(e) => setForm({ ...form, gender: e.target.value })} placeholder="Gender" required style={fieldStyle} />
          <input type="date" value={form.date_of_birth} onChange={(e) => setForm({ ...form, date_of_birth: e.target.value })} required style={fieldStyle} />
          <input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} placeholder="Phone" required style={fieldStyle} />
          <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} placeholder="Email" required style={fieldStyle} />
          <input value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} placeholder="Address" required style={fieldStyle} />
          <input type="date" value={form.registration_date} onChange={(e) => setForm({ ...form, registration_date: e.target.value })} required style={fieldStyle} />
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

export default Patients;
