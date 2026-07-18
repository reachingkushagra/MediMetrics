import React from 'react';

const StatCard = ({ label, value, tone = 'primary' }) => {
  const tones = {
    primary: '#2563EB',
    success: '#22C55E',
    warning: '#F59E0B',
    danger: '#EF4444',
    secondary: '#14B8A6',
  };

  return (
    <div style={{ background: '#fff', border: '1px solid #E2E8F0', borderRadius: '14px', padding: '16px' }}>
      <div style={{ color: '#64748B', fontSize: '13px' }}>{label}</div>
      <div style={{ marginTop: '8px', fontSize: '20px', fontWeight: 700, color: tones[tone] }}>{value}</div>
    </div>
  );
};

export default StatCard;
