import React from 'react';

const SearchBar = ({ value, onChange, placeholder }) => (
  <input
    type="text"
    value={value}
    onChange={onChange}
    placeholder={placeholder}
    style={{
      width: '100%',
      maxWidth: '320px',
      padding: '10px 14px',
      borderRadius: '10px',
      border: '1px solid #E2E8F0',
      outline: 'none',
      fontSize: '14px',
    }}
  />
);

export default SearchBar;
