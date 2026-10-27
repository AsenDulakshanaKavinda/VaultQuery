import React, { useState } from 'react';
import '../../styles/auth.css'
import { Link, useNavigate } from 'react-router-dom';
import { PasswordReset } from './PasswordReset';

export function LoginScreen({ onLoginSuccess }) {
  // States to preview different UI variations shown in the spec:
  // 'default', 'error', 'loading', 'focused', 'locked'
  const [stateMode, setStateMode] = useState('default');
  
  const [email, setEmail] = useState('alex.morgan@example.com');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setStateMode('loading');
    setTimeout(() => {
      if (onLoginSuccess) onLoginSuccess();
    }, 1500);
  };


  const navigate = useNavigate();

  const handleForgotPasswordClick = (e) => {
    e.preventDefault();
    navigate('/password-reset')
  }

  const handleRequestAccessClick = (e) => {
    e.preventDefault();
    navigate('/request-access')
  }


  return (
    <div className="login-container">
      {/* Left Hero / Brand Panel */}
      <div className="login-left-panel">
        <div className="login-brand-header">
          <svg className="login-brand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
          </svg>
          <span>VaultQuery</span>
        </div>

        <div className="login-hero-content">
          <h1 className="login-hero-title">Ask anything.<br />See only what you’re allowed to.</h1>
          <div className="login-features-list">
            <div className="login-feature-item">
              <span>✓</span> Answers cite their sources
            </div>
            <div className="login-feature-item">
              <span>✓</span> Access follows your ACL
            </div>
            <div className="login-feature-item">
              <span>✓</span> Every query is audited
            </div>
          </div>
        </div>

        <div className="login-footer-meta">
          <span>Permission-aware intelligence</span>
          <span>VTL · SECURE ACCESS</span>
        </div>
      </div>

      {/* Right Login Form Panel */}
      <div className="login-right-panel">
        <div className="login-form-wrapper">
          {/* Quick Demo Controller for Viewing Spec States */}
          <div style={{ marginBottom: '16px', display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
            <button onClick={() => setStateMode('default')} style={{ fontSize: '10px', padding: '2px 6px' }}>Default</button>
            <button onClick={() => setStateMode('error')} style={{ fontSize: '10px', padding: '2px 6px' }}>Error</button>
            <button onClick={() => setStateMode('loading')} style={{ fontSize: '10px', padding: '2px 6px' }}>Loading</button>
            <button onClick={() => setStateMode('locked')} style={{ fontSize: '10px', padding: '2px 6px' }}>Locked</button>
          </div>

          <div className="login-top-label">VaultQuery / Secure Access</div>

          <h2 className="login-form-title">Welcome back</h2>
          <p className="login-form-subtitle">Sign in to your permission-aware workspace.</p>

          {/* Error Banner */}
          {stateMode === 'error' && (
            <div className="login-alert login-alert-error">
              <span>⚠️</span>
              <span>Email or password is incorrect.</span>
            </div>
          )}

          {/* Temporarily Locked Banner */}
          {stateMode === 'locked' && (
            <div className="login-alert login-alert-warning">
              <span>🔒</span>
              <div>
                <strong>Account temporarily locked</strong>
                <p style={{ margin: '4px 0 0 0', fontSize: '12px' }}>
                  For your security, sign-in is paused after repeated attempts. Wait 15 minutes before trying again, or reset your password. Contact your administrator if you need help.
                </p>
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="login-field">
              <label className="login-label">Work email</label>
              <input
                type="email"
                className="login-input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="alex.morgan@example.com"
                required
              />
            </div>

            <div className="login-field">
              <label className="login-label">Password</label>
              <div className="login-input-container">
                <input
                  type="password"
                  className="login-input"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  required
                />
                <button type="button" className="login-input-icon-right" aria-label="Show password">
                  👁️
                </button>
              </div>
            </div>

            <div className="login-options-row">
              <label className="login-checkbox-label">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                />
                <span>Remember me 30 days</span>
              </label>
              <a href="/password-reset" className="login-link" onClick={handleForgotPasswordClick}>Forgot password?</a>
            </div>

            <button type="submit" className="login-submit-btn" disabled={stateMode === 'loading'}>
              {stateMode === 'loading' ? 'Signing in...' : 'Sign in'}
            </button>
          </form>

          <div className="login-divider">or</div>

          <button type="button" className="login-sso-btn">
            <span>🏢</span> Continue with company SSO
          </button>

          <div className="login-register-prompt">
            New here? <a href="/request-access" className="login-link" onClick={handleRequestAccessClick}>Request access</a>
          </div>

          <div className="login-bottom-meta">
            <span>Protected access. Privacy by design.</span>
            <span>VTL / SECURE</span>
          </div>
        </div>
      </div>
    </div>
  );
}