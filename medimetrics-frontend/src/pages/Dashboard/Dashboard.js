import React, { useEffect, useState } from 'react';
import DashboardCard from '../../components/DashboardCard/DashboardCard';
import Loader from '../../components/Loader/Loader';
import StatCard from '../../components/StatCard/StatCard';
import { getAppointmentStatus, getAverageConsultationTime, getAverageWaitTime, getDashboardStats, getDepartmentAppointments, getDoctorWorkload, getPeakHours } from '../../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [waitTime, setWaitTime] = useState(null);
  const [consultationTime, setConsultationTime] = useState(null);
  const [doctorWorkload, setDoctorWorkload] = useState([]);
  const [departmentAppointments, setDepartmentAppointments] = useState([]);
  const [peakHours, setPeakHours] = useState([]);
  const [statusData, setStatusData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [dashboardRes, waitRes, consultationRes, workloadRes, deptRes, peakRes, statusRes] = await Promise.all([
          getDashboardStats(),
          getAverageWaitTime(),
          getAverageConsultationTime(),
          getDoctorWorkload(),
          getDepartmentAppointments(),
          getPeakHours(),
          getAppointmentStatus(),
        ]);

        setStats(dashboardRes.data);
        setWaitTime(waitRes.data);
        setConsultationTime(consultationRes.data);
        setDoctorWorkload(workloadRes.data || []);
        setDepartmentAppointments(deptRes.data || []);
        setPeakHours(peakRes.data || []);
        setStatusData(statusRes.data || []);
      } catch (err) {
        setError('Unable to load dashboard analytics right now.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <Loader />;
  if (error) return <div style={{ padding: '24px', color: '#EF4444' }}>{error}</div>;

  return (
    <div>
      <div style={{ background: '#fff', borderRadius: '20px', padding: '24px', border: '1px solid #E2E8F0', marginBottom: '20px', boxShadow: '0 8px 24px rgba(15,23,42,0.04)' }}>
        <h2 style={{ margin: '0 0 8px', color: '#0F172A' }}>Welcome to MediMetrics</h2>
        <p style={{ margin: 0, color: '#64748B' }}>A live overview of appointments, care team performance, and hospital operations.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px', marginBottom: '24px' }}>
        <DashboardCard title="Total Patients" value={stats?.total_patients ?? 0} subtitle="Registered patients" accent="#2563EB" />
        <DashboardCard title="Total Doctors" value={stats?.total_doctors ?? 0} subtitle="Active medical staff" accent="#14B8A6" />
        <DashboardCard title="Total Departments" value={stats?.total_departments ?? 0} subtitle="Clinical units" accent="#F59E0B" />
        <DashboardCard title="Total Appointments" value={stats?.total_appointments ?? 0} subtitle="Scheduled visits" accent="#22C55E" />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px', marginBottom: '24px' }}>
        <StatCard label="Average Wait Time" value={`${waitTime?.average_wait_time_minutes ?? 0} min`} tone="primary" />
        <StatCard label="Average Consultation Time" value={`${consultationTime?.average_consultation_minutes ?? 0} min`} tone="secondary" />
        <StatCard label="Peak Hours" value={peakHours[0] ? `${peakHours[0].hour}:00` : '—'} tone="warning" />
      </div>

      <div style={{ display: 'grid', gap: '16px' }}>
        <div style={{ background: '#fff', borderRadius: '16px', padding: '20px', border: '1px solid #E2E8F0', boxShadow: '0 6px 24px rgba(15,23,42,0.05)' }}>
          <h3 style={{ marginTop: 0 }}>Doctor Workload</h3>
          {doctorWorkload.length === 0 ? <div>No records found</div> : (
            <div style={{ display: 'grid', gap: '10px' }}>
              {doctorWorkload.map((item) => (
                <div key={item.doctor} style={{ display: 'flex', justifyContent: 'space-between', paddingBottom: '8px', borderBottom: '1px solid #F1F5F9' }}>
                  <span>{item.doctor}</span>
                  <strong>{item.total_appointments}</strong>
                </div>
              ))}
            </div>
          )}
        </div>

        <div style={{ background: '#fff', borderRadius: '16px', padding: '20px', border: '1px solid #E2E8F0', boxShadow: '0 6px 24px rgba(15,23,42,0.05)' }}>
          <h3 style={{ marginTop: 0 }}>Department Appointments</h3>
          {departmentAppointments.length === 0 ? <div>No records found</div> : (
            <div style={{ display: 'grid', gap: '10px' }}>
              {departmentAppointments.map((item) => (
                <div key={item.department_name} style={{ display: 'flex', justifyContent: 'space-between', paddingBottom: '8px', borderBottom: '1px solid #F1F5F9' }}>
                  <span>{item.department_name}</span>
                  <strong>{item.total_appointments}</strong>
                </div>
              ))}
            </div>
          )}
        </div>

        <div style={{ background: '#fff', borderRadius: '16px', padding: '20px', border: '1px solid #E2E8F0', boxShadow: '0 6px 24px rgba(15,23,42,0.05)' }}>
          <h3 style={{ marginTop: 0 }}>Appointment Status</h3>
          {statusData.length === 0 ? <div>No records found</div> : (
            <div style={{ display: 'grid', gap: '10px' }}>
              {statusData.map((item) => (
                <div key={item.status_name} style={{ display: 'flex', justifyContent: 'space-between', paddingBottom: '8px', borderBottom: '1px solid #F1F5F9' }}>
                  <span>{item.status_name}</span>
                  <strong>{item.total}</strong>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
