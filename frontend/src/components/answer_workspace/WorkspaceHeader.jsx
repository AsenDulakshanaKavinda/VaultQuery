import React from 'react';
import { useTheme } from '../../theme/ThemeContext';
import '../../styles/workspace.css'

export function WorkspaceHeader({ orgName = "VTL", workspaceName = "Knowledge workspace", roleName = "Account Managers & Ops Supervisors" }) {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="vault-navbar">
      {/* Breadcrumbs */}
      <div className="vault-breadcrumb">
        <span className="vault-breadcrumb-org">{orgName}</span>
        <span className="vault-breadcrumb-separator">/</span>
        <span className="vault-breadcrumb-workspace">{workspaceName}</span>
      </div>

      {/* Right Action Bar */}
      <div className="vault-navbar-right">
        {/* Permission / Scope Badge */}
        <div className="vault-permission-badge">
          <svg
            className="vault-permission-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
            <polyline points="22 4 12 14.01 9 11.01" />
          </svg>
          <span>{roleName}</span>
        </div>

        {/* Divider */}
        <div className="vault-navbar-divider" />

        {/* Action Icons */}
        <div className="vault-navbar-actions">
          {/* Theme Switcher Button */}
          <button
            onClick={toggleTheme}
            className="vault-icon-btn"
            title={theme === 'dark' ? "Switch to Light Mode" : "Switch to Dark Mode"}
            aria-label="Toggle Theme"
          >
            {theme === 'dark' ? (
              /* Sun Icon for Light Mode */
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="4" />
                <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M18.36 5.64l1.41-1.41" />
              </svg>
            ) : (
              /* Gear/Sun-styled outline icon matching your spec header */
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="4" />
                <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M18.36 5.64l1.41-1.41" />
              </svg>
            )}
          </button>

          {/* Help Icon */}
          <button
            className="vault-icon-btn"
            title="Help & Info"
            aria-label="Help"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10" />
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
              <line x1="12" y1="17" x2="12.01" y2="17" />
            </svg>
          </button>
        </div>
      </div>
    </header>
  );
}