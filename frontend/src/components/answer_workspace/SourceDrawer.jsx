import React, { useState } from 'react';
import '../../styles/workspace.css'

export function SourceDrawer({ onClose }) {
  const [activeTab, setActiveTab] = useState('excerpt');

  return (
    <aside className="source-drawer">
      {/* Drawer Header */}
      <div className="drawer-header">
        <span className="drawer-title">Source evidence</span>
        <button onClick={onClose} className="close-btn" aria-label="Close panel">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      {/* Document Info Header */}
      <div className="source-badge">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
          <line x1="16" y1="13" x2="8" y2="13" />
          <line x1="16" y1="17" x2="8" y2="17" />
        </svg>
        <span>SHAREPOINT · CITATION [1]</span>
      </div>

      <h2 className="doc-title">Apex Automotive Corp — Rotterdam recovery SOP</h2>
      <div className="doc-version">Version 3.2 · Updated 16 Oct 2026</div>

      <button className="sharepoint-btn">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
          <polyline points="15 3 21 3 21 9" />
          <line x1="10" y1="14" x2="21" y2="3" />
        </svg>
        <span>Open in SharePoint</span>
      </button>

      {/* Navigation Tabs */}
      <div className="drawer-tabs">
        <button
          className={`tab-btn ${activeTab === 'excerpt' ? 'active' : ''}`}
          onClick={() => setActiveTab('excerpt')}
        >
          Excerpt
        </button>
        <button
          className={`tab-btn ${activeTab === 'details' ? 'active' : ''}`}
          onClick={() => setActiveTab('details')}
        >
          Document details
        </button>
      </div>

      {activeTab === 'excerpt' ? (
        <>
          {/* Supports Step Callout Card */}
          <div className="supports-card">
            <div className="supports-tag">SUPPORTS ANSWER · STEP 1</div>
            <p className="supports-text">
              Target the next sailing within 24 hours; wait for carrier confirmation before sharing an ETA.
            </p>
          </div>

          {/* Direct Quote Block */}
          <div className="excerpt-section">
            <div className="section-label-sm">PAGE 7 · § 4.2 MISSED CUTOFF</div>
            <blockquote className="quote-block">
              “For Apex Automotive Corp shipments, target the next available sailing within 24 hours of a missed Rotterdam cutoff. Communicate the revised delivery ETA only once the carrier has confirmed the booking.”
            </blockquote>
          </div>
        </>
      ) : (
        <div style={{ padding: '12px 0', fontSize: '13px', color: 'var(--text-muted)' }}>
          Detailed document metadata and access logs...
        </div>
      )}

      {/* Metadata Grid */}
      <div className="meta-grid">
        <div className="meta-item">
          <span className="meta-label">Owner</span>
          <span className="meta-value">VTL European Operations</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">Last synced</span>
          <span className="meta-value">19 Oct, 13:15 UTC</span>
        </div>
        <div className="meta-item" style={{ gridColumn: 'span 2' }}>
          <span className="meta-label">Location</span>
          <span className="meta-value-mono">Operations / Europe / Rotterdam / Apex</span>
        </div>
      </div>

      {/* Permission Check Footer */}
      <div className="access-footer">
        <svg className="access-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
          <polyline points="22 4 12 14.01 9 11.01" />
        </svg>
        <span>Available to you through your VTL work account.</span>
      </div>
    </aside>
  );
}