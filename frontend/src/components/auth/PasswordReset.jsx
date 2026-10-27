import React, { useState } from 'react';
import '../../styles/auth.css'
import { useNavigate } from 'react-router-dom';

export function PasswordReset({ onBackToLogin }) {
  // Step modes corresponding to screenshot designs:
  // 1: 'enter_email'
  // 2: 'check_email'
  // 3: 'set_password'
  // 4: 'success'
  const [step, setStep] = useState('enter_email');

  const [email, setEmail] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSendResetLink = (e) => {
    e.preventDefault();
    setStep('check_email');
  };

  const handleSetNewPassword = (e) => {
    e.preventDefault();
    setStep('success');
  };

  const navigate = useNavigate();

  const handleBackToSignInClick = (e) => {
    e.preventDefault();
    navigate('/')
  }

  return (
    <div className="reset-container">
      {/* Left Brand Panel */}
      <div className="reset-left-panel">
        <div className="reset-brand-header">
          <svg className="reset-brand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
          </svg>
          <span>VaultQuery</span>
        </div>

        <div className="reset-hero-content">
          <h1 className="reset-hero-title">Ask anything.<br />See only what you’re allowed to.</h1>
          <div className="reset-features-list">
            <div className="reset-feature-item">
              <span>✓</span> Answers cite their sources
            </div>
            <div className="reset-feature-item">
              <span>✓</span> Access follows your role
            </div>
            <div className="reset-feature-item">
              <span>✓</span> Every query is audited
            </div>
          </div>
        </div>

        <div className="reset-footer-meta">
          <span>Permission-aware intelligence</span>
          <span>VTL / SECURE</span>
        </div>
      </div>

      {/* Right Form Panel */}
      <div className="reset-right-panel">
        <div className="reset-form-wrapper">
          {/* Demo Step Switcher */}
          <div style={{ marginBottom: '16px', display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
            <button onClick={() => setStep('enter_email')} style={{ fontSize: '10px', padding: '2px 6px' }}>Step 1: Enter email</button>
            <button onClick={() => setStep('check_email')} style={{ fontSize: '10px', padding: '2px 6px' }}>Step 2: Check email</button>
            <button onClick={() => setStep('set_password')} style={{ fontSize: '10px', padding: '2px 6px' }}>Step 3: New password</button>
            <button onClick={() => setStep('success')} style={{ fontSize: '10px', padding: '2px 6px' }}>Step 4: Success</button>
          </div>

          <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '24px', textTransform: 'uppercase' }}>
            VaultQuery / Secure Access
          </div>

          {/* --- STEP 1: ENTER EMAIL --- */}
          {step === 'enter_email' && (
            <>
              <div className="reset-step-indicator">PASSWORD RECOVERY · STEP 1 OF 3</div>
              <h2 className="reset-title">Reset your password</h2>
              <p className="reset-subtitle">Enter your work email to request a password reset link.</p>

              <form onSubmit={handleSendResetLink}>
                <div className="reset-field">
                  <label className="reset-label">Work email</label>
                  <input
                    type="email"
                    className="reset-input"
                    placeholder="you@company.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>

                <button type="submit" className="reset-btn-primary">
                  Send reset link
                </button>
              </form>

              <button type="button" className="reset-back-link" onClick={handleBackToSignInClick}>
                ← Back to sign in
              </button>
            </>
          )}

          {/* --- STEP 2: CHECK YOUR EMAIL --- */}
          {step === 'check_email' && (
            <>
              <div className="mail-icon-wrapper">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                  <polyline points="22,6 12,13 2,6" />
                </svg>
              </div>

              <div className="reset-step-indicator">PASSWORD RECOVERY · STEP 2 OF 3</div>
              <h2 className="reset-title">Check your email</h2>
              <p className="reset-subtitle">
                If an account exists for that email address, you’ll receive a link to reset your password.
              </p>

              <div className="reset-callout-box">
                <div className="reset-callout-title">Don’t see an email?</div>
                <div className="reset-callout-text">
                  Check your spam folder or try again in a few minutes. For help, contact your administrator.
                </div>
              </div>

              <button type="button" className="reset-btn-secondary" onClick={() => setStep('enter_email')}>
                Try another email
              </button>

              <button type="button" className="reset-back-link" onClick={handleBackToSignInClick}>
                ← Back to sign in
              </button>
            </>
          )}

          {/* --- STEP 3: SET A NEW PASSWORD --- */}
          {step === 'set_password' && (
            <>
              <div className="reset-step-indicator">PASSWORD RECOVERY · STEP 3 OF 3</div>
              <h2 className="reset-title">Set a new password</h2>
              <p className="reset-subtitle">Choose a strong password you haven’t used before.</p>

              <form onSubmit={handleSetNewPassword}>
                <div className="reset-field">
                  <label className="reset-label">New password</label>
                  <div className="reset-input-container">
                    <input
                      type="password"
                      className="reset-input"
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
                      placeholder="••••••••••••"
                      required
                    />
                    <button type="button" className="reset-input-icon-right">👁️</button>
                  </div>

                  {/* Password Strength Indicator */}
                  <div className="password-strength-bar">
                    <div className="strength-segment active" />
                    <div className="strength-segment active" />
                    <div className="strength-segment active" />
                    <div className="strength-segment active" />
                  </div>
                  <div className="strength-label">Strong password</div>

                  <div className="password-rules">
                    <div className="rule-item"><span>✓</span> At least 12 characters</div>
                    <div className="rule-item"><span>✓</span> Uppercase and lowercase letters</div>
                    <div className="rule-item"><span>✓</span> A number and a symbol</div>
                  </div>
                </div>

                <div className="reset-field">
                  <label className="reset-label">Confirm new password</label>
                  <div className="reset-input-container">
                    <input
                      type="password"
                      className="reset-input"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      placeholder="••••••••••••"
                      required
                    />
                    <button type="button" className="reset-input-icon-right">👁️</button>
                  </div>
                  <div className="match-status"><span>✓</span> Passwords match</div>
                </div>

                <button type="submit" className="reset-btn-primary">
                  Reset password
                </button>
              </form>

              <button type="button" className="reset-back-link" onClick={handleBackToSignInClick}>
                ← Back to sign in
              </button>
            </>
          )}

          {/* --- STEP 4: SUCCESS --- */}
          {step === 'success' && (
            <div style={{ textAlign: 'center' }}>
              <div className="success-icon-wrapper" style={{ margin: '0 auto 20px auto' }}>✓</div>
              <h2 className="reset-title">Password updated</h2>
              <p className="reset-subtitle">
                Your new password is ready. Sign in to securely access your workspace.
              </p>

              <button type="button" className="reset-btn-primary" onClick={handleBackToSignInClick}>
                Back to sign in
              </button>
            </div>
          )}

          <div style={{ marginTop: '32px', textAlign: 'center', fontSize: '11px', color: 'var(--text-muted)' }}>
            Protected access. Privacy by design.
          </div>
        </div>
      </div>
    </div>
  );
}