import React from 'react';

export function RegisterTable({ requests, onSelectRequest }) {
  return (
    <div className="reg-table-container">
      <table className="reg-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Requested At</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {requests.length === 0 ? (
            <tr>
              <td colSpan="4" style={{ textAlign: 'center', padding: '32px', color: 'var(--text-muted)' }}>
                No register requests found.
              </td>
            </tr>
          ) : (
            requests.map((req) => (
              <tr key={req.id} onClick={() => onSelectRequest(req)}>
                <td style={{ fontWeight: 500 }}>{req.name}</td>
                <td>{req.email}</td>
                <td>{req.requestedAt}</td>
                <td>
                  <span className={`reg-status-chip ${req.status}`}>
                    <span className="reg-status-dot" />
                    {req.status.charAt(0).toUpperCase() + req.status.slice(1)}
                  </span>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}