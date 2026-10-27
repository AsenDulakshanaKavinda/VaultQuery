import React, { useState } from 'react';
import '../../styles/auth.css'
import { useNavigate } from 'react-router-dom';

export function RequestAccess({ onBackToLogin }) {
  // Modes for viewing states shown in screenshot: 'default', 'errors', 'success'
  const [viewState, setViewState] = useState('default');

  const [fullName, setFullName] = useState('');
  const [workEmail, setWorkEmail] = useState('');
  const [password, setPassword] = useState('');
  const [agreedTerms, setAgreedTerms] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (viewState === 'errors') {
      return;
    }
    setViewState('success');
  };

  const navigate = useNavigate();

  const handleBackToSignInClick = (e) => {
    e.preventDefault();
    navigate('/')
  }




  return (
    <div className="request-access-container">
      {/* Left Brand Panel */}
      <div className="request-left-panel">
        <div className="request-brand-header">
          <svg className="request-brand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
          </svg>
          <span>VaultQuery</span>
        </div>

        <div className="request-hero-content">
          <h1 className="request-hero-title">Ask anything.<br />See only what you’re allowed to.</h1>
          <div className="request-features-list">
            <div className="request-feature-item">
              <span>✓</span> Answers cite their sources
            </div>
            <div className="request-feature-item">
              <span>✓</span> Access follows your role
            </div>
            <div className="request-feature-item">
              <span>✓</span> Every query is audited
            </div>
          </div>
        </div>

        <div className="request-footer-meta">
          <span>Permission-aware intelligence</span>
          <span>VTL / SECURE</span>
        </div>
      </div>

      {/* Right Form Panel */}
      <div className="request-right-panel">
        <div className="request-form-wrapper">
          {/* Quick Demo Controller for Spec States */}
          <div style={{ marginBottom: '16px', display: 'flex', gap: '6px' }}>
            <button onClick={() => setViewState('default')} style={{ fontSize: '10px', padding: '2px 6px' }}>Default</button>
            <button onClick={() => { setViewState('errors'); setWorkEmail('alex.morgan'); setPassword('123'); }} style={{ fontSize: '10px', padding: '2px 6px' }}>Validation Errors</button>
            <button onClick={() => setViewState('success')} style={{ fontSize: '10px', padding: '2px 6px' }}>Success State</button>
          </div>

          <div className="request-top-label">VaultQuery / Secure Access</div>

          {viewState === 'success' ? (
            /* --- Success View State --- */
            <div className="success-wrapper">
              <div className="success-icon-circle">✓</div>
              <h2 className="success-title">Request submitted</h2>
              <p className="success-description">
                Request submitted. You’ll get an email once an administrator approves your access.
                <br /><br />
                Your access level is assigned by your administrator after approval.
              </p>
              <button className="request-submit-btn" onClick={handleSignInClick}>
                Back to sign in
              </button>
            </div>
          ) : (
            /* --- Form View State (Default & Errors) --- */
            <>
              <h2 className="request-form-title">Request access</h2>
              <p className="request-form-subtitle">Create your account to get started with VaultQuery.</p>

              <form onSubmit={handleSubmit}>
                <div className="request-field">
                  <label className="request-label">Full name</label>
                  <input
                    type="text"
                    className={`request-input ${viewState === 'errors' && !fullName ? 'request-input-error' : ''}`}
                    placeholder="Enter your full name"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                  />
                  {viewState === 'errors' && !fullName && (
                    <span className="field-error-msg">Enter your full name.</span>
                  )}
                </div>

                <div className="request-field">
                  <label className="request-label">Work email</label>
                  <input
                    type="text"
                    className={`request-input ${viewState === 'errors' ? 'request-input-error' : ''}`}
                    placeholder="you@company.com"
                    value={workEmail}
                    onChange={(e) => setWorkEmail(e.target.value)}
                  />
                  {viewState === 'errors' && (
                    <span className="field-error-msg">Enter a valid work email address.</span>
                  )}
                </div>

                <div className="request-field">
                  <label className="request-label">Password</label>
                  <div className="request-input-container">
                    <input
                      type="password"
                      className={`request-input ${viewState === 'errors' ? 'request-input-error' : ''}`}
                      placeholder="Create a password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                    />
                    <button type="button" className="request-input-icon-right">👁️</button>
                  </div>

                  {viewState === 'errors' && (
                    <span className="field-error-msg">Choose a password that meets all requirements.</span>
                  )}

                  {/* Password Strength Indicator */}
                  <div className="password-strength-bar">
                    <div className={`strength-segment ${viewState === 'errors' ? 'active-danger' : 'active'}`} />
                    <div className="strength-segment" />
                    <div className="strength-segment" />
                    <div className="strength-segment" />
                  </div>

                  <div className="password-rules">
                    <div className="rule-item">Password requirements:</div>
                    <div className={`rule-item ${viewState === 'errors' ? 'invalid' : ''}`}>
                      <span>•</span> At least 12 characters
                    </div>
                    <div className={`rule-item ${viewState === 'errors' ? 'valid' : ''}`}>
                      <span>✓</span> Uppercase and lowercase letters
                    </div>
                    <div className={`rule-item ${viewState === 'errors' ? 'invalid' : ''}`}>
                      <span>•</span> A number and a symbol
                    </div>
                  </div>
                </div>

                <div className="terms-row">
                  <label className="terms-label">
                    <input
                      type="checkbox"
                      checked={agreedTerms}
                      onChange={(e) => setAgreedTerms(e.target.checked)}
                    />
                    <span>I agree to the <a href="#terms" className="request-link">Terms of use</a> and <a href="#privacy" className="request-link">Privacy policy</a>.</span>
                  </label>
                  {viewState === 'errors' && !agreedTerms && (
                    <div className="field-error-msg" style={{ marginTop: '4px' }}>Agree to the terms to request access.</div>
                  )}
                </div>

                <button type="submit" className="request-submit-btn">
                  Request access
                </button>
              </form>

              <div className="request-info-note">
                Your access level is assigned by your administrator after approval.
              </div>

              <div className="request-login-prompt">
                Already have an account?{' '}
                <button
                  type="button"
                  className="request-link"
                  onClick={handleBackToSignInClick}
                  style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0, font: 'inherit' }}
                >
                  Sign in
                </button>
              </div>

              <div style={{ marginTop: '32px', textAlign: 'center', fontSize: '11px', color: 'var(--text-muted)' }}>
                Protected access. Privacy by design.
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}