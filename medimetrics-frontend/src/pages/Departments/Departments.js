import React, { useEffect, useMemo, useState } from 'react';
import Button from '../../components/Button/Button';
import DataTable from '../../components/DataTable/DataTable';
import Loader from '../../components/Loader/Loader';
import Modal from '../../components/Modal/Modal';
import PageHeader from '../../components/PageHeader/PageHeader';
import SearchBar from '../../components/SearchBar/SearchBar';
import { createDepartment, deleteDepartment, getDepartments, updateDepartment } from '../../services/api';

const emptyForm = {
  department_name: '',
  location: '',
};

const Departments = () => {
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [modalOpen, setModalOpen] = useState(false);
  const [editingDepartment, setEditingDepartment] = useState(null);
  const [form, setForm] = useState(emptyForm);

  const fetchDepartments = async () => {
    try {
      setLoading(true);
      const response = await getDepartments();
      setDepartments(response.data || []);
    } catch (err) {
      setError('Unable to load departments.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDepartments();
  }, []);

  const filteredDepartments = useMemo(() => {
    const term = search.toLowerCase();
    return departments.filter((department) => `${department.department_name} ${department.location}`.toLowerCase().includes(term));
  }, [departments, search]);

  const handleOpenCreate = () => {
    setEditingDepartment(null);
    setForm(emptyForm);
    setModalOpen(true);
  };

  const handleOpenEdit = (department) => {
    setEditingDepartment(department);
    setForm({ department_name: department.department_name || '', location: department.location || '' });
    setModalOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingDepartment) {
        await updateDepartment(editingDepartment.department_id, form);
      } else {
        await createDepartment(form);
      }
      setModalOpen(false);
      fetchDepartments();
    } catch (err) {
      setError('The request could not be completed.');
    }
  };

  const handleDelete = async (departmentId) => {
    try {
      await deleteDepartment(departmentId);
      fetchDepartments();
    } catch (err) {
      setError('Unable to delete department.');
    }
  };

  const columns = [
    { header: 'Department ID', key: 'department_id' },
    { header: 'Department Name', key: 'department_name' },
    { header: 'Location', key: 'location' },
    {
      header: 'Actions',
      key: 'actions',
      render: (row) => (
        <div style={{ display: 'flex', gap: '8px' }}>
          <Button variant="outline" onClick={() => handleOpenEdit(row)}>Edit</Button>
          <Button variant="danger" onClick={() => handleDelete(row.department_id)}>Delete</Button>
        </div>
      ),
    },
  ];

  return (
    <div>
      <PageHeader title="Departments" subtitle="Track hospital units and locations" actionLabel="Add Department" onAction={handleOpenCreate} />
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', gap: '12px', flexWrap: 'wrap' }}>
        <SearchBar value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search departments" />
      </div>
      {error && <div style={{ color: '#EF4444', marginBottom: '12px' }}>{error}</div>}
      {loading ? <Loader /> : <DataTable columns={columns} data={filteredDepartments} emptyMessage="No Records Found" />}

      <Modal open={modalOpen} title={editingDepartment ? 'Edit Department' : 'Add Department'} onClose={() => setModalOpen(false)}>
        <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '12px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px' }}>
            <input value={form.department_name} onChange={(e) => setForm({ ...form, department_name: e.target.value })} placeholder="Department Name" required style={fieldStyle} />
            <input value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} placeholder="Location" required style={fieldStyle} />
          </div>
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

export default Departments;
