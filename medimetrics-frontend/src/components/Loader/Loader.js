import React from 'react';

const Loader = () => (
  <div style={{ display: 'flex', justifyContent: 'center', padding: '24px' }}>
    <div
      style={{
        width: '40px',
        height: '40px',
        border: '4px solid #E2E8F0',
        borderTop: '4px solid #2563EB',
        borderRadius: '50%',
        animation: 'spin 1s linear infinite',
      }}
    />
  </div>
);

export default Loader;
