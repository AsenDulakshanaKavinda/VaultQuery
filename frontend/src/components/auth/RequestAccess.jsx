import React, { useState } from 'react';
import '../../styles/auth.css';
import { useNavigate } from 'react-router-dom';
import { 
  KeyRound, 
  Eye, 
  EyeOff, 
  CheckCircle2, 
  Check, 
  X, 
  AlertCircle 
} from 'lucide-react';

export function RequestAccess({ onBackToLogin }) {
  // Modes for viewing demo states: 'default', 'errors', 'success'
  const [viewState, setViewState] = useState('default');

  const [fullName, setFullName] = useState('');
  const [workEmail, setWorkEmail] = useState('');
  const [password, setPassword] = useState('');
  const [agreedTerms, setAgreedTerms] = useState(false);
  
  // UI toggles & API state
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState('');

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
  const navigate = useNavigate();

  const handleBackToSignInClick = (e) => {
    if (e) e.preventDefault();
    navigate('/');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError('');

    // Basic validation check
    if (!fullName || !workEmail || !password || !agreedTerms) {
      setViewState('errors');
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/request-access`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          fullName,
          email: workEmail,
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to submit access request.');
      }

      setViewState('success');
    } catch (err) {
      console.error('Request access error:', err);
      setApiError(err.message || 'Something went wrong. Please try again.');
      setViewState('errors');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="request-access-container">
      {/* Left Brand Panel */}
      <div className="request-left-panel">
        <div className="request-brand-header">
          <KeyRound className="request-brand-icon" size={24} />
          <span>VaultQuery</span>
        </div>

        <div className="request-hero-content">
          <h1 className="request-hero-title">Ask anything.<br />See only what you’re allowed to.</h1>
          <div className="request-features-list">
            <div className="request-feature-item">
              <Check size={16} className="feature-check" /> Answers cite their sources
            </div>
            <div className="request-feature-item">
              <Check size={16} className="feature-check" /> Access follows your role
            </div>
            <div className="request-feature-item">
              <Check size={16} className="feature-check" /> Every query is audited
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
            <button type="button" onClick={() => { setViewState('default'); setApiError(''); }} style={{ fontSize: '10px', padding: '2px 6px' }}>Default</button>
            <button type="button" onClick={() => { setViewState('errors'); setWorkEmail('alex.morgan'); setPassword('123'); }} style={{ fontSize: '10px', padding: '2px 6px' }}>Validation Errors</button>
            <button type="button" onClick={() => { setViewState('success'); setApiError(''); }} style={{ fontSize: '10px', padding: '2px 6px' }}>Success State</button>
          </div>

          <div className="request-top-label">VaultQuery / Secure Access</div>

          {apiError && (
            <div style={{ color: '#ef4444', marginBottom: '16px', fontSize: '13px', background: 'rgba(239, 68, 68, 0.1)', padding: '10px', borderRadius: '6px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <AlertCircle size={16} />
              <span>{apiError}</span>
            </div>
          )}

          {viewState === 'success' ? (
            /* --- Success View State --- */
            <div className="success-wrapper" style={{ textAlign: 'center' }}>
              <div className="success-icon-circle" style={{ margin: '0 auto 20px auto', display: 'flex', justifyContent: 'center' }}>
                <CheckCircle2 size={48} color="#10b981" />
              </div>
              <h2 className="success-title">Request submitted</h2>
              <p className="success-description">
                Request submitted. You’ll get an email once an administrator approves your access.
                <br /><br />
                Your access level is assigned by your administrator after approval.
              </p>
              <button type="button" className="request-submit-btn" onClick={handleBackToSignInClick}>
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
                    <span className="field-error-msg" style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: '4px', color: '#ef4444', fontSize: '12px' }}>
                      <AlertCircle size={12} /> Enter your full name.
                    </span>
                  )}
                </div>

                <div className="request-field">
                  <label className="request-label">Work email</label>
                  <input
                    type="text"
                    className={`request-input ${viewState === 'errors' && (!workEmail || !workEmail.includes('@')) ? 'request-input-error' : ''}`}
                    placeholder="you@company.com"
                    value={workEmail}
                    onChange={(e) => setWorkEmail(e.target.value)}
                  />
                  {viewState === 'errors' && (!workEmail || !workEmail.includes('@')) && (
                    <span className="field-error-msg" style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: '4px', color: '#ef4444', fontSize: '12px' }}>
                      <AlertCircle size={12} /> Enter a valid work email address.
                    </span>
                  )}
                </div>

                <div className="request-field">
                  <label className="request-label">Password</label>
                  <div className="request-input-container" style={{ position: 'relative' }}>
                    <input
                      type={showPassword ? 'text' : 'password'}
                      className={`request-input ${viewState === 'errors' && password.length < 12 ? 'request-input-error' : ''}`}
                      placeholder="Create a password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                    />
                    <button
                      type="button"
                      className="request-input-icon-right"
                      onClick={() => setShowPassword(!showPassword)}
                      aria-label={showPassword ? 'Hide password' : 'Show password'}
                      style={{ background: 'none', border: 'none', cursor: 'pointer', position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)' }}
                    >
                      {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>

                  {viewState === 'errors' && password.length < 12 && (
                    <span className="field-error-msg" style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: '4px', color: '#ef4444', fontSize: '12px' }}>
                      <AlertCircle size={12} /> Choose a password that meets all requirements.
                    </span>
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
                    <div className={`rule-item ${viewState === 'errors' ? 'invalid' : ''}`} style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                      {viewState === 'errors' ? <X size={12} color="#ef4444" /> : <span>•</span>} At least 12 characters
                    </div>
                    <div className={`rule-item ${viewState === 'errors' ? 'valid' : ''}`} style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <Check size={12} color="#10b981" /> Uppercase and lowercase letters
                    </div>
                    <div className={`rule-item ${viewState === 'errors' ? 'invalid' : ''}`} style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                      {viewState === 'errors' ? <X size={12} color="#ef4444" /> : <span>•</span>} A number and a symbol
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
                    <div className="field-error-msg" style={{ marginTop: '4px', color: '#ef4444', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <AlertCircle size={12} /> Agree to the terms to request access.
                    </div>
                  )}
                </div>

                <button type="submit" className="request-submit-btn" disabled={isLoading}>
                  {isLoading ? 'Submitting request...' : 'Request access'}
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