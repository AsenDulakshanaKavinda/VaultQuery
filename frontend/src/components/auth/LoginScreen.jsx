import React, { useState } from 'react';
import '../../styles/auth.css';
import { useNavigate } from 'react-router-dom';
import { 
  KeyRound, 
  Eye, 
  EyeOff, 
  AlertTriangle, 
  Lock, 
  Building2, 
  Check, 
  ShieldCheck 
} from 'lucide-react';

export function LoginScreen({ onLoginSuccess }) {
  // Demo state mode for previewing UI variations: 'default', 'error', 'loading', 'locked'
  const [stateMode, setStateMode] = useState('default');

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState('Email or password is incorrect.');

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
  const navigate = useNavigate();

  const handleForgotPasswordClick = (e) => {
    e.preventDefault();
    navigate('/password-reset');
  };

  const handleRequestAccessClick = (e) => {
    e.preventDefault();
    navigate('/request-access');
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setStateMode('loading');

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 423) {
          setStateMode('locked');
          throw new Error(data.message || 'Account temporarily locked.');
        }
        throw new Error(data.message || 'Failed to sign in');
      }

      // Success: Save token and trigger callback
      localStorage.setItem('token', data.token);
      setStateMode('default');
      if (onLoginSuccess) {
        onLoginSuccess(data);
      }
    } catch (err) {
      console.error('Login error:', err);
      setErrorMessage(err.message || 'Email or password is incorrect.');
      if (stateMode !== 'locked') {
        setStateMode('error');
      }
    }
  };

  return (
    <div className="login-container">
      {/* Left Hero / Brand Panel */}
      <div className="login-left-panel">
        <div className="login-brand-header">
          <KeyRound className="login-brand-icon" size={24} />
          <span>VaultQuery</span>
        </div>

        <div className="login-hero-content">
          <h1 className="login-hero-title">Ask anything.<br />See only what you’re allowed to.</h1>
          <div className="login-features-list">
            <div className="login-feature-item">
              <Check size={16} className="feature-check" /> Answers cite their sources
            </div>
            <div className="login-feature-item">
              <Check size={16} className="feature-check" /> Access follows your ACL
            </div>
            <div className="login-feature-item">
              <Check size={16} className="feature-check" /> Every query is audited
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
            <button type="button" onClick={() => setStateMode('default')} style={{ fontSize: '10px', padding: '2px 6px' }}>Default</button>
            <button type="button" onClick={() => setStateMode('error')} style={{ fontSize: '10px', padding: '2px 6px' }}>Error</button>
            <button type="button" onClick={() => setStateMode('loading')} style={{ fontSize: '10px', padding: '2px 6px' }}>Loading</button>
            <button type="button" onClick={() => setStateMode('locked')} style={{ fontSize: '10px', padding: '2px 6px' }}>Locked</button>
          </div>

          <div className="login-top-label">VaultQuery / Secure Access</div>

          <h2 className="login-form-title">Welcome back</h2>
          <p className="login-form-subtitle">Sign in to your permission-aware workspace.</p>

          {/* Error Banner */}
          {stateMode === 'error' && (
            <div className="login-alert login-alert-error" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <AlertTriangle size={18} style={{ flexShrink: 0 }} />
              <span>{errorMessage}</span>
            </div>
          )}

          {/* Temporarily Locked Banner */}
          {stateMode === 'locked' && (
            <div className="login-alert login-alert-warning" style={{ display: 'flex', gap: '10px', alignItems: 'flex-start' }}>
              <Lock size={18} style={{ flexShrink: 0, marginTop: '2px' }} />
              <div>
                <strong>Account temporarily locked</strong>
                <p style={{ margin: '4px 0 0 0', fontSize: '12px' }}>
                  For your security, sign-in is paused after repeated attempts. Wait 15 minutes before trying again, or reset your password. Contact your administrator if you need help.
                </p>
              </div>
            </div>
          )}

          <form onSubmit={handleLoginSubmit}>
            <div className="login-field">
              <label className="login-label">Work email</label>
              <input
                type="email"
                className="login-input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@company.com"
                required
              />
            </div>

            <div className="login-field">
              <label className="login-label">Password</label>
              <div className="login-input-container" style={{ position: 'relative' }}>
                <input
                  type={showPassword ? 'text' : 'password'}
                  className="login-input"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  required
                />
                <button
                  type="button"
                  className="login-input-icon-right"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                  style={{ background: 'none', border: 'none', cursor: 'pointer', position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)' }}
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
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

            <button type="submit" className="login-submit-btn" disabled={stateMode === 'loading' || stateMode === 'locked'}>
              {stateMode === 'loading' ? 'Signing in...' : 'Sign in'}
            </button>
          </form>

          <div className="login-divider">or</div>

          <button type="button" className="login-sso-btn" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
            <Building2 size={16} /> Continue with company SSO
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