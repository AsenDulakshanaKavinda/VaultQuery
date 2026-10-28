import React, { useState } from 'react';
import '../../styles/auth.css';
import { useNavigate } from 'react-router-dom';
import { 
  KeyRound, 
  Mail, 
  CheckCircle2, 
  ArrowLeft, 
  Eye, 
  EyeOff, 
  ShieldCheck, 
  Check, 
  X 
} from 'lucide-react';

export function PasswordReset({ onBackToLogin }) {
  const [step, setStep] = useState('enter_email');

  const [email, setEmail] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  // UI state toggles
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
  const navigate = useNavigate();

  const handleBackToSignInClick = (e) => {
    e.preventDefault();
    navigate('/');
  };

  // STEP 1: Submit email to request reset link
  const handleSendResetLink = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/forgot-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to send password reset link.');
      }

      setStep('check_email');
    } catch (err) {
      console.error('Password reset error:', err);
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // STEP 3: Submit new password update
  const handleSetNewPassword = async (e) => {
    e.preventDefault();
    setError('');

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/reset-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, newPassword }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to update password.');
      }

      setStep('success');
    } catch (err) {
      console.error('Password update error:', err);
      setError(err.message || 'Failed to reset password. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="reset-container">
      {/* Left Brand Panel */}
      <div className="reset-left-panel">
        <div className="reset-brand-header">
          <KeyRound className="reset-brand-icon" size={24} />
          <span>VaultQuery</span>
        </div>

        <div className="reset-hero-content">
          <h1 className="reset-hero-title">Ask anything.<br />See only what you’re allowed to.</h1>
          <div className="reset-features-list">
            <div className="reset-feature-item">
              <Check size={16} className="feature-check" /> Answers cite their sources
            </div>
            <div className="reset-feature-item">
              <Check size={16} className="feature-check" /> Access follows your role
            </div>
            <div className="reset-feature-item">
              <Check size={16} className="feature-check" /> Every query is audited
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
            <button onClick={() => { setStep('enter_email'); setError(''); }} style={{ fontSize: '10px', padding: '2px 6px' }}>Step 1: Enter email</button>
            <button onClick={() => { setStep('check_email'); setError(''); }} style={{ fontSize: '10px', padding: '2px 6px' }}>Step 2: Check email</button>
            <button onClick={() => { setStep('set_password'); setError(''); }} style={{ fontSize: '10px', padding: '2px 6px' }}>Step 3: New password</button>
            <button onClick={() => { setStep('success'); setError(''); }} style={{ fontSize: '10px', padding: '2px 6px' }}>Step 4: Success</button>
          </div>

          <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '24px', textTransform: 'uppercase' }}>
            VaultQuery / Secure Access
          </div>

          {error && (
            <div style={{ color: '#ef4444', marginBottom: '16px', fontSize: '13px', background: 'rgba(239, 68, 68, 0.1)', padding: '10px', borderRadius: '6px' }}>
              {error}
            </div>
          )}

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

                <button type="submit" className="reset-btn-primary" disabled={isLoading}>
                  {isLoading ? 'Sending...' : 'Send reset link'}
                </button>
              </form>

              <button type="button" className="reset-back-link" onClick={handleBackToSignInClick}>
                <ArrowLeft size={16} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '4px' }} />
                Back to sign in
              </button>
            </>
          )}

          {/* --- STEP 2: CHECK YOUR EMAIL --- */}
          {step === 'check_email' && (
            <>
              <div className="mail-icon-wrapper" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Mail size={24} />
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

              <button type="button" className="reset-btn-secondary" onClick={() => { setStep('enter_email'); setError(''); }}>
                Try another email
              </button>

              <button type="button" className="reset-back-link" onClick={handleBackToSignInClick}>
                <ArrowLeft size={16} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '4px' }} />
                Back to sign in
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
                  <div className="reset-input-container" style={{ position: 'relative' }}>
                    <input
                      type={showPassword ? 'text' : 'password'}
                      className="reset-input"
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
                      placeholder="••••••••••••"
                      required
                    />
                    <button 
                      type="button" 
                      className="reset-input-icon-right" 
                      onClick={() => setShowPassword(!showPassword)}
                      style={{ background: 'none', border: 'none', cursor: 'pointer', position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)' }}
                    >
                      {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
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
                    <div className="rule-item"><Check size={14} /> At least 12 characters</div>
                    <div className="rule-item"><Check size={14} /> Uppercase and lowercase letters</div>
                    <div className="rule-item"><Check size={14} /> A number and a symbol</div>
                  </div>
                </div>

                <div className="reset-field">
                  <label className="reset-label">Confirm new password</label>
                  <div className="reset-input-container" style={{ position: 'relative' }}>
                    <input
                      type={showConfirmPassword ? 'text' : 'password'}
                      className="reset-input"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      placeholder="••••••••••••"
                      required
                    />
                    <button 
                      type="button" 
                      className="reset-input-icon-right" 
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      style={{ background: 'none', border: 'none', cursor: 'pointer', position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)' }}
                    >
                      {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                  <div className="match-status" style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: '6px' }}>
                    {newPassword && confirmPassword && newPassword === confirmPassword ? (
                      <span style={{ color: '#10b981', display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <Check size={14} /> Passwords match
                      </span>
                    ) : confirmPassword ? (
                      <span style={{ color: '#ef4444', display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <X size={14} /> Passwords do not match
                      </span>
                    ) : null}
                  </div>
                </div>

                <button type="submit" className="reset-btn-primary" disabled={isLoading}>
                  {isLoading ? 'Resetting...' : 'Reset password'}
                </button>
              </form>

              <button type="button" className="reset-back-link" onClick={handleBackToSignInClick}>
                <ArrowLeft size={16} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '4px' }} />
                Back to sign in
              </button>
            </>
          )}

          {/* --- STEP 4: SUCCESS --- */}
          {step === 'success' && (
            <div style={{ textAlign: 'center' }}>
              <div className="success-icon-wrapper" style={{ margin: '0 auto 20px auto', display: 'flex', justifyContent: 'center' }}>
                <CheckCircle2 size={48} color="#10b981" />
              </div>
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