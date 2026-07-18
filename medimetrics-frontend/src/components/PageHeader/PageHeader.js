import React from 'react';
import Button from '../Button/Button';

const PageHeader = ({ title, subtitle, actionLabel, onAction }) => (
  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', gap: '12px', flexWrap: 'wrap' }}>
    <div>
      <h2 style={{ margin: 0, color: '#0F172A' }}>{title}</h2>
      {subtitle && <p style={{ margin: '4px 0 0', color: '#64748B' }}>{subtitle}</p>}
    </div>
    {actionLabel && onAction && <Button onClick={onAction}>{actionLabel}</Button>}
  </div>
);

export default PageHeader;
