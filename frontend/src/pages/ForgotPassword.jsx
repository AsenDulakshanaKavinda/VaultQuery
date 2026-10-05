import { useState } from "react";
import { Link } from "react-router-dom";
import AuthLayout from "../components/AuthLayout.jsx";
import Field from "../components/Field.jsx";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      // TODO: replace with your API call, e.g.
      // await fetch("/api/auth/forgot-password", {
      //   method: "POST",
      //   headers: { "Content-Type": "application/json" },
      //   body: JSON.stringify({ email }),
      // });
      console.log("reset requested for", email);
      setSent(true);
    } catch (err) {
      setError(err.message || "Could not send the reset link. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout>
      {sent ? (
        <div className="auth-form">
          <h1>Check your email</h1>
          <p className="auth-sub">
            If an account exists for <strong>{email}</strong>, we've sent a link
            to reset your password.
          </p>
          <p className="auth-switch">
            <Link to="/login">Back to login</Link>
          </p>
        </div>
      ) : (
        <form className="auth-form" onSubmit={handleSubmit}>
          <h1>Reset password</h1>
          <p className="auth-sub">
            Enter your email and we'll send you a link to reset your password.
          </p>

          <Field
            label="Email"
            type="email"
            name="email"
            placeholder="you@company.com"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          {error && <p className="auth-error" role="alert">{error}</p>}

          <button className="btn-primary" type="submit" disabled={loading}>
            {loading ? "Sending…" : "Send reset link"}
          </button>

          <p className="auth-switch">
            <Link to="/login">Back to login</Link>
          </p>
        </form>
      )}
    </AuthLayout>
  );
}