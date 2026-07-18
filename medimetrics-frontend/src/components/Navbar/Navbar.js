import React from 'react';

const Navbar = () => (
  <header style={{ background: '#fff', padding: '16px 24px', borderBottom: '1px solid #E2E8F0', display: 'flex', justifyContent: 'space-between', alignItems: 'center', position: 'sticky', top: 0, zIndex: 10, boxShadow: '0 2px 10px rgba(15,23,42,0.04)' }}>
    <div>
      <div style={{ color: '#0F172A', fontWeight: 700, fontSize: '18px' }}>Hospital Operations</div>
      <div style={{ color: '#64748B', fontSize: '13px' }}>Healthcare dashboard and scheduling overview</div>
    </div>
    <div style={{ color: '#2563EB', fontWeight: 700, background: '#EFF6FF', padding: '8px 12px', borderRadius: '999px' }}>Live Data</div>
  </header>
);

export default Navbar;
