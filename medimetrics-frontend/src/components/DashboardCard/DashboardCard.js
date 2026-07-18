import React from 'react';

const DashboardCard = ({ title, value, subtitle, accent }) => (
  <div style={{ background: '#fff', borderRadius: '16px', padding: '20px', boxShadow: '0 6px 24px rgba(15,23,42,0.06)', border: '1px solid #E2E8F0' }}>
    <div style={{ color: '#64748B', fontSize: '13px', marginBottom: '8px' }}>{title}</div>
    <div style={{ fontSize: '28px', fontWeight: 700, color: '#0F172A' }}>{value}</div>
    {subtitle && <div style={{ color: accent || '#2563EB', fontSize: '13px', marginTop: '8px' }}>{subtitle}</div>}
  </div>
);

export default DashboardCard;
