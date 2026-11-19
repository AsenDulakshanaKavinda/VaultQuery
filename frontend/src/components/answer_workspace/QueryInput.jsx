import React, { useState } from 'react';
import '../../styles/workspace.css'

export function QueryInput({ onSend, placeholder = "Ask a follow-up about this answer..." }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && onSend) {
      onSend(query);
      setQuery('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form className="query-input-card" onSubmit={handleSubmit}>
      {/* Input Field */}
      <textarea
        className="query-textarea"
        rows={2}
        placeholder={placeholder}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
      />

      {/* Footer Controls */}
      <div className="query-input-footer">
        {/* Left: Sources Trigger */}
        <button type="button" className="sources-btn">
          <svg className="sources-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <ellipse cx="12" cy="5" rx="9" ry="3" />
            <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
            <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
          </svg>
          <span>Your available sources</span>
        </button>

        {/* Right: Send Action */}
        <button type="submit" className="send-btn">
          <svg className="send-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="19" x2="12" y2="5" />
            <polyline points="5 12 12 5 19 12" />
          </svg>
          <span>Send</span>
        </button>
      </div>
    </form>
  );
}