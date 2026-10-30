import React, { useState } from 'react';

export function RegisterSidebar({ request, onClose, onSubmit }) {
  const [selectedRole, setSelectedRole] = useState(request.role || 'Account Manager');
  const [selectedCompany, setSelectedCompany] = useState(request.company || 'Vanguard Transit & Logistics');

  const handleFormSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      ...request,
      role: selectedRole,
      company: selectedCompany,
      status: 'approved',
      updatedAt: new Date().toISOString().replace('T', ' ').substring(0, 16) + ' UTC',
    });
  };

  return (
    <div className="reg-drawer-backdrop" onClick={onClose}>
      <div className="reg-drawer" onClick={(e) => e.stopPropagation()}>
        <div className="reg-drawer-header">
          <h3 className="reg-drawer-title">Request Details</h3>
          <button className="reg-drawer-close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="reg-drawer-body">
          <div className="reg-detail-group">
            <span className="reg-detail-label">Request ID</span>
            <span className="reg-detail-value">{request.id}</span>
          </div>

          <div className="reg-detail-group">
            <span className="reg-detail-label">Name</span>
            <span className="reg-detail-value" style={{ fontFamily: 'var(--font-sans)', fontWeight: 600, fontSize: '16px' }}>
              {request.name}
            </span>
          </div>

          <div className="reg-detail-group">
            <span className="reg-detail-label">Email</span>
            <span className="reg-detail-value">{request.email}</span>
          </div>

          <div className="reg-detail-group">
            <span className="reg-detail-label">Requested At</span>
            <span className="reg-detail-value">{request.requestedAt}</span>
          </div>

          <div className="reg-detail-group">
            <span className="reg-detail-label">Updated At</span>
            <span className="reg-detail-value">{request.updatedAt}</span>
          </div>

          <hr style={{ border: 'none', borderTop: '1px solid var(--border)', margin: '4px 0' }} />

          <form id="approval-form" onSubmit={handleFormSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div className="reg-detail-group">
              <label className="reg-detail-label">Select Role</label>
              <select
                className="reg-form-select"
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
              >
                <option value="Account Manager">Account Manager</option>
                <option value="Ops Supervisor">Ops Supervisor</option>
                <option value="Security Administrator">Security Administrator</option>
                <option value="Logistics Operator">Logistics Operator</option>
              </select>
            </div>

            <div className="reg-detail-group">
              <label className="reg-detail-label">Select Company / Workspace</label>
              <select
                className="reg-form-select"
                value={selectedCompany}
                onChange={(e) => setSelectedCompany(e.target.value)}
              >
                <option value="Vanguard Transit & Logistics">Vanguard Transit & Logistics</option>
                <option value="Apex Automotive Corp">Apex Automotive Corp</option>
                <option value="Rotterdam Port Authority">Rotterdam Port Authority</option>
                <option value="OmniRetail Holdings">OmniRetail Holdings</option>
              </select>
            </div>
          </form>
        </div>

        <div className="reg-drawer-footer">
          <button type="submit" form="approval-form" className="reg-btn-primary">
            Approve & Assign
          </button>
          <button type="button" className="reg-btn-secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}