import React, { useState } from 'react';
import '../../styles/workspace.css'

export function SidebarLeft() {
  const [activeNav, setActiveNav] = useState('ask');
  const [activeConvo, setActiveConvo] = useState(1);

  const recentConversations = [
    { id: 1, title: 'Apex Rotterdam recovery', time: 'Today' },
    { id: 2, title: 'Nova Pharma Global handover', time: 'Yesterday' },
    { id: 3, title: 'OmniRetail Holdings delivery windows', time: '16 Oct' },
    { id: 4, title: 'Singapore warehouse checklist', time: '16 Oct' },
  ];

  return (
    <aside className="vault-sidebar">
      {/* Brand Header */}
      <div className="sidebar-header">
        <svg className="brand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
        </svg>
        <span className="brand-title">VaultQuery</span>
      </div>

      {/* Workspace Details */}
      <div className="workspace-info">
        <div className="workspace-title">Vanguard Transit & Logistics</div>
        <div className="workspace-subtitle">EMPLOYEE WORKSPACE</div>
      </div>

      {/* Primary Actions */}
      <div className="action-buttons">
        <button className="btn-new-convo">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          <span>New conversation</span>
        </button>

        <button 
          className={`nav-item ${activeNav === 'ask' ? 'active' : ''}`}
          onClick={() => setActiveNav('ask')}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
          <span>Ask VaultQuery</span>
        </button>

        <button 
          className={`nav-item ${activeNav === 'sources' ? 'active' : ''}`}
          onClick={() => setActiveNav('sources')}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
          </svg>
          <span>Browse sources</span>
        </button>
      </div>

      {/* Recent Conversations List */}
      <div className="section-label">Recent Conversations</div>
      <div className="recent-list">
        {recentConversations.map((convo) => (
          <div
            key={convo.id}
            className={`convo-item ${activeConvo === convo.id ? 'active' : ''}`}
            onClick={() => setActiveConvo(convo.id)}
          >
            <span className="convo-title">{convo.title}</span>
            <span className="convo-time">{convo.time}</span>
          </div>
        ))}
      </div>

      {/* Footer Section */}
      <div className="sidebar-footer">
        <div className="help-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
            <line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
          <span>Help & guidance</span>
        </div>

        <div className="footer-divider" />

        <div className="user-profile">
          <div className="avatar">MC</div>
          <div className="user-details">
            <span className="user-name">Maya Chen</span>
            <span className="user-role">Account Manager · Chicago HQ</span>
          </div>
        </div>
      </div>
    </aside>
  );
}