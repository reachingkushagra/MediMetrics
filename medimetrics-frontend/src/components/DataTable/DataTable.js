import React from 'react';

const DataTable = ({ columns, data, emptyMessage }) => {
  if (!data || data.length === 0) {
    return <div style={{ padding: '20px', textAlign: 'center', color: '#64748B' }}>{emptyMessage}</div>;
  }

  return (
    <div style={{ overflowX: 'auto', borderRadius: '16px', border: '1px solid #E2E8F0', background: '#fff' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead style={{ background: '#F8FAFC' }}>
          <tr>
            {columns.map((column) => (
              <th key={column.key} style={{ textAlign: 'left', padding: '12px 14px', color: '#475569', fontSize: '13px' }}>
                {column.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={row.id || index} style={{ borderTop: '1px solid #E2E8F0' }}>
              {columns.map((column) => (
                <td key={`${row.id || index}-${column.key}`} style={{ padding: '12px 14px', color: '#0F172A' }}>
                  {column.render ? column.render(row) : row[column.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataTable;
