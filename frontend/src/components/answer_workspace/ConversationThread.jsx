import React, { useState } from 'react';
import { StatusChip } from '../PrimaryBtn'; 
import '../../styles/workspace.css'

export function ConversationThread({ onSelectSource }) {
  const [selectedSourceId, setSelectedSourceId] = useState(1);

  const sources = [
    {
      id: 1,
      title: 'Apex Automotive Corp — Rotterdam recovery SOP',
      type: 'SharePoint',
      version: 'v3.2',
      updated: '16 Oct 2026',
      iconType: 'document',
    },
    {
      id: 2,
      title: '#rotterdam-ops · Apex recovery coordination',
      type: 'Slack thread',
      updated: '19 Oct 2026, 13:05 UTC',
      iconType: 'external',
    },
    {
      id: 3,
      title: 'OPS-2841 · Apex missed cutoff recovery',
      type: 'Jira ticket',
      updated: '19 Oct 2026, 13:12 UTC',
      iconType: 'external',
    },
  ];

  const handleSourceClick = (id) => {
    setSelectedSourceId(id);
    if (onSelectSource) {
      onSelectSource(id);
    }
  };

  return (
    <div className="conversation-container">
      {/* Thread Header */}
      <div className="thread-header">
        <div>
          <h1 className="thread-title">Apex Rotterdam recovery</h1>
          <div className="thread-meta">Today, 19 Oct 2026 · 08:20 CDT</div>
        </div>
        <button className="icon-menu-btn" aria-label="More options">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="1" />
            <circle cx="19" cy="12" r="1" />
            <circle cx="5" cy="12" r="1" />
          </svg>
        </button>
      </div>

      {/* User Question */}
      <div className="user-msg-box">
        <div className="user-avatar">MC</div>
        <p className="user-msg-text">
          What should I tell Apex Automotive Corp about the missed Rotterdam cutoff, and what happens next?
        </p>
      </div>

      {/* AI Answer Block */}
      <div className="ai-response-block">
        <div className="ai-header">
          <div className="ai-brand">
            <svg className="ai-brand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
            </svg>
            <span>VaultQuery</span>
          </div>
          <StatusChip type="success" label="3 supporting sources" />
        </div>

        <div className="ai-content">
          <p>
            Tell Apex that VTL is coordinating recovery from Rotterdam. The terminal shuttle is booked; the revised delivery ETA is still awaiting carrier confirmation.
          </p>
          <ol>
            <li>
              <strong>1. Set the expectation.</strong> VTL targets the next available sailing within 24 hours of a missed cutoff. Share a revised ETA only after the carrier confirms it.{' '}
              <span className="citation-badge" onClick={() => handleSourceClick(1)}>[1]</span>
            </li>
            <li>
              <strong>2. Explain the recovery.</strong> The Rotterdam team has booked the 13:30 UTC shuttle to the terminal and is coordinating the next sailing with the carrier.{' '}
              <span className="citation-badge" onClick={() => handleSourceClick(2)}>[2]</span>
            </li>
            <li>
              <strong>3. Commit to the next update.</strong> Priya Nair owns OPS-2841. Send Apex a status update by 14:00 UTC today, even if carrier confirmation is still pending.{' '}
              <span className="citation-badge" onClick={() => handleSourceClick(3)}>[3]</span>
            </li>
          </ol>
        </div>

        {/* Action Controls */}
        <div className="ai-actions-row">
          <button className="action-btn-text">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
            </svg>
            <span>Copy answer</span>
          </button>
          
          <button className="action-btn-icon" aria-label="Thumbs up">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3" />
            </svg>
          </button>

          <button className="action-btn-icon" aria-label="Thumbs down">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h3a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-3" />
            </svg>
          </button>

          <span>Based on source updates through 19 Oct, 13:12 UTC</span>
        </div>
      </div>

      {/* Supporting Sources Section */}
      <div className="sources-section-header">
        <span className="sources-label">SUPPORTING SOURCES</span>
        <span className="sources-hint">Select a source to review evidence</span>
      </div>

      <div className="sources-list">
        {sources.map((src) => (
          <div
            key={src.id}
            className={`source-card ${selectedSourceId === src.id ? 'selected' : ''}`}
            onClick={() => handleSourceClick(src.id)}
          >
            <div className="source-card-left">
              <span className="source-num">{src.id}</span>
              <div className="source-details">
                <span className="source-title">{src.title}</span>
                <span className="source-meta">
                  {src.type} {src.version ? `· ${src.version}` : ''} · Updated {src.updated}
                </span>
              </div>
            </div>

            <div className="source-icon">
              {src.iconType === 'document' ? (
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                </svg>
              ) : (
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                  <polyline points="15 3 21 3 21 9" />
                  <line x1="10" y1="14" x2="21" y2="3" />
                </svg>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}