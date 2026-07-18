import React, { useEffect, useMemo, useState } from 'react';
import Button from '../../components/Button/Button';
import DataTable from '../../components/DataTable/DataTable';
import Loader from '../../components/Loader/Loader';
import Modal from '../../components/Modal/Modal';
import PageHeader from '../../components/PageHeader/PageHeader';
import SearchBar from '../../components/SearchBar/SearchBar';
import { createDoctor, deleteDoctor, getDepartments, getDoctors, updateDoctor } from '../../services/api';

const emptyForm = {
  first_name: '',
  last_name: '',
  specialization: '',
  phone: '',
  email: '',
  department_id: '',
};

const Doctors = () => {
  const [doctors, setDoctors] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [modalOpen, setModalOpen] = useState(false);
  const [editingDoctor, setEditingDoctor] = useState(null);
  const [form, setForm] = useState(emptyForm);

  const fetchDoctors = async () => {
    try {
      setLoading(true);
      const [doctorResponse, departmentResponse] = await Promise.all([getDoctors(), getDepartments()]);
      setDoctors(doctorResponse.data || []);
      setDepartments(departmentResponse.data || []);
    } catch (err) {
      setError('Unable to load doctors.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDoctors();
  }, []);

  const filteredDoctors = useMemo(() => {
    const term = search.toLowerCase();
    return doctors.filter((doctor) => `${doctor.first_name} ${doctor.last_name} ${doctor.specialization}`.toLowerCase().includes(term));
  }, [doctors, search]);

  const handleOpenCreate = () => {
    setEditingDoctor(null);
    setForm(emptyForm);
    setModalOpen(true);
  };

  const handleOpenEdit = (doctor) => {
    setEditingDoctor(doctor);
    setForm({
      first_name: doctor.first_name || '',
      last_name: doctor.last_name || '',
      specialization: doctor.specialization || '',
      phone: doctor.phone || '',
      email: doctor.email || '',
      department_id: doctor.department_id || '',
    });
    setModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = { ...form, department_id: Number(form.department_id) };
      if (editingDoctor) {
        await updateDoctor(editingDoctor.doctor_id, payload);
      } else {
        await createDoctor(payload);
      }
      setModalOpen(false);
      fetchDoctors();
    } catch (err) {
      setError('The request could not be completed.');
    }
  };

  const handleDelete = async (doctorId) => {
    try {
      await deleteDoctor(doctorId);
      fetchDoctors();
    } catch (err) {
      setError('Unable to delete doctor.');
    }
  };

  const departmentMap = Object.fromEntries(departments.map((department) => [department.department_id, department.department_name]));

  const columns = [
    { header: 'Doctor ID', key: 'doctor_id' },
    { header: 'Doctor Name', key: 'first_name', render: (row) => `${row.first_name} ${row.last_name}` },
    { header: 'Specialization', key: 'specialization' },
    { header: 'Department', key: 'department_id', render: (row) => departmentMap[row.department_id] || row.department_id },
    { header: 'Phone', key: 'phone' },
    { header: 'Email', key: 'email' },
    {
      header: 'Actions',
      key: 'actions',
      render: (row) => (
        <div style={{ display: 'flex', gap: '8px' }}>
          <Button variant="outline" onClick={() => handleOpenEdit(row)}>Edit</Button>
          <Button variant="danger" onClick={() => handleDelete(row.doctor_id)}>Delete</Button>
        </div>
      ),
    },
  ];

  return (
    <div>
      <PageHeader title="Doctors" subtitle="Review physician profiles and coverage" actionLabel="Add Doctor" onAction={handleOpenCreate} />
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', gap: '12px', flexWrap: 'wrap' }}>
        <SearchBar value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search doctors" />
      </div>
      {error && <div style={{ color: '#EF4444', marginBottom: '12px' }}>{error}</div>}
      {loading ? <Loader /> : <DataTable columns={columns} data={filteredDoctors} emptyMessage="No Records Found" />}

      <Modal open={modalOpen} title={editingDoctor ? 'Edit Doctor' : 'Add Doctor'} onClose={() => setModalOpen(false)}>
        <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '12px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px' }}>
            <input value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} placeholder="First Name" required style={fieldStyle} />
            <input value={form.last_name} onChange={(e) => setForm({ ...form, last_name: e.target.value })} placeholder="Last Name" required style={fieldStyle} />
          </div>
          <input value={form.specialization} onChange={(e) => setForm({ ...form, specialization: e.target.value })} placeholder="Specialization" required style={fieldStyle} />
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px' }}>
            <input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} placeholder="Phone" required style={fieldStyle} />
            <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} placeholder="Email" required style={fieldStyle} />
          </div>
          <select value={form.department_id} onChange={(e) => setForm({ ...form, department_id: e.target.value })} required style={fieldStyle}>
            <option value="">Select Department</option>
            {departments.map((department) => (
              <option key={department.department_id} value={department.department_id}>{department.department_name}</option>
            ))}
          </select>
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

export default Doctors;
