import React, { useState } from 'react';
import { RegisterTable } from '../components/RegisterTable';
import { RegisterSidebar } from '../components/RegisterSidebar';
import '../styles/app.css';

const INITIAL_REQUESTS = [
  { id: 'REQ-5091', name: 'Maya Chen', email: 'maya.chen@vtl.com', requestedAt: '19 Oct 2026, 08:20 UTC', updatedAt: '19 Oct 2026, 08:20 UTC', status: 'pending', role: 'Account Manager', company: 'Vanguard Transit & Logistics' },
  { id: 'REQ-5092', name: 'Alex Morgan', email: 'alex.morgan@apex.com', requestedAt: '18 Oct 2026, 14:15 UTC', updatedAt: '19 Oct 2026, 09:00 UTC', status: 'approved', role: 'Ops Supervisor', company: 'Apex Automotive Corp' },
  { id: 'REQ-5093', name: 'David Kim', email: 'dkim@rotterdamport.nl', requestedAt: '17 Oct 2026, 11:30 UTC', updatedAt: '17 Oct 2026, 16:45 UTC', status: 'rejected', role: 'Logistics Operator', company: 'Rotterdam Port Authority' },
  { id: 'REQ-5094', name: 'Priya Nair', email: 'priya.nair@vtl.com', requestedAt: '16 Oct 2026, 09:10 UTC', updatedAt: '16 Oct 2026, 10:20 UTC', status: 'pending', role: 'Security Administrator', company: 'Vanguard Transit & Logistics' },
  { id: 'REQ-5095', name: 'Liam Jansen', email: 'liam.j@omni.retail', requestedAt: '15 Oct 2026, 17:50 UTC', updatedAt: '15 Oct 2026, 18:00 UTC', status: 'approved', role: 'Account Manager', company: 'OmniRetail Holdings' },
];

export function RegisterRequestsPage() {
  const [requests, setRequests] = useState(INITIAL_REQUESTS);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [selectedRequest, setSelectedRequest] = useState(null);

  // Filter requests based on search query and status filter
  const filteredRequests = requests.filter((req) => {
    const matchesSearch = req.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          req.email.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === 'all' || req.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const handleUpdateSubmission = (updatedReq) => {
    setRequests(requests.map((r) => (r.id === updatedReq.id ? updatedReq : r)));
    setSelectedRequest(null);
  };

  return (
    <div className="reg-page-container">
      <div className="reg-main-content">
        <div className="reg-header-area">
          <h1 className="reg-title">Register Requests</h1>
          <p className="reg-subtitle">Review, search, and manage incoming user onboarding applications.</p>

          <div className="reg-controls-row">
            {/* Search Input */}
            <div className="reg-search-box">
              <svg className="reg-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="11" cy="11" r="8" />
                <line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
              <input
                type="text"
                className="reg-search-input"
                placeholder="Search by name or email..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>

            {/* Status Filter Dropdown */}
            <select
              className="reg-filter-select"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="all">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
        </div>

        {/* Requests Table List */}
        <RegisterTable requests={filteredRequests} onSelectRequest={setSelectedRequest} />
      </div>

      {/* Slide-over Detail Sidebar */}
      {selectedRequest && (
        <RegisterSidebar
          request={selectedRequest}
          onClose={() => setSelectedRequest(null)}
          onSubmit={handleUpdateSubmission}
        />
      )}
    </div>
  );
}