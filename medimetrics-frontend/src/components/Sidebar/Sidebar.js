import React from 'react';
import { NavLink } from 'react-router-dom';
import logo from "../../logo.png";


const navItems = [
  { path: '/', label: 'Dashboard' },
  { path: '/patients', label: 'Patients' },
  { path: '/doctors', label: 'Doctors' },
  { path: '/departments', label: 'Departments' },
  { path: '/appointments', label: 'Appointments' },
];

const Sidebar = () => (
  <aside style={{ width: '280px', minHeight: '100vh', background: 'linear-gradient(180deg, #0F172A 0%, #111827 100%)', color: '#fff', padding: '24px 20px', position: 'sticky', top: 0, boxShadow: '0 10px 30px rgba(15,23,42,0.15)' }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '28px' }}>
      <img src={logo} alt="MediMetrics Logo" className="logo" style={{ width: '48px', height: '48px', borderRadius: '12px' }} />
      <div>
        <div style={{ fontSize: '20px', fontWeight: 700 }}>MediMetrics</div>
        <div style={{ fontSize: '12px', color: '#CBD5E1', lineHeight: 1.4 }}>Smart Patient Appointment & Wait Time Analytics</div>
      </div>
    </div>

    <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      {navItems.map((item) => (
        <NavLink
          key={item.path}
          to={item.path}
          style={({ isActive }) => ({
            textDecoration: 'none',
            color: isActive ? '#fff' : '#CBD5E1',
            background: isActive ? '#2563EB' : 'transparent',
            padding: '12px 14px',
            borderRadius: '10px',
            fontWeight: 600,
            transition: 'all 0.2s ease',
          })}
        >
          {item.label}
        </NavLink>
      ))}
    </nav>
  </aside>
);

export default Sidebar;
