import React from 'react';

const Button = ({ children, onClick, variant = 'primary', type = 'button', disabled = false }) => {
  const variants = {
    primary: { background: '#2563EB', color: '#fff' },
    secondary: { background: '#14B8A6', color: '#fff' },
    danger: { background: '#EF4444', color: '#fff' },
    outline: { background: '#fff', color: '#2563EB', border: '1px solid #BFDBFE' },
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      style={{
        ...variants[variant],
        border: 'none',
        borderRadius: '10px',
        padding: '10px 16px',
        cursor: disabled ? 'not-allowed' : 'pointer',
        fontWeight: 600,
        opacity: disabled ? 0.7 : 1,
      }}
    >
      {children}
    </button>
  );
};

export default Button;
