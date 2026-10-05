import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthLayout from "../components/AuthLayout.jsx";
import Field from "../components/Field.jsx";
import { useAuth } from "../context/AuthContext.jsx";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) =>
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      // TODO: replace with your API call, e.g.
      // const res = await fetch("/api/auth/login", {
      //   method: "POST",
      //   headers: { "Content-Type": "application/json" },
      //   body: JSON.stringify(form),
      // });
      // if (!res.ok) throw new Error((await res.json()).message);
      // Until the backend exists, the name is faked from the email.
      // With a real API, use the user object it returns instead:
      // login(await res.json()); // expects { name, email }
      login({ name: form.email.split("@")[0], email: form.email });
      navigate("/", { replace: true });
    } catch (err) {
      setError(err.message || "Could not log in. Check your details and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout>
      <form className="auth-form" onSubmit={handleSubmit}>
        <h1>Login</h1>
        <p className="auth-sub">Welcome back! Please enter your details.</p>

        <Field
          label="Email"
          type="email"
          name="email"
          placeholder="you@company.com"
          autoComplete="email"
          value={form.email}
          onChange={handleChange}
          required
        />
        <Field
          label="Password"
          type="password"
          name="password"
          placeholder="Enter your password"
          autoComplete="current-password"
          value={form.password}
          onChange={handleChange}
          required
        />

        <div className="auth-row">
          <Link to="/forgot-password">Forgot password?</Link>
        </div>

        {error && <p className="auth-error" role="alert">{error}</p>}

        <button className="btn-primary" type="submit" disabled={loading}>
          {loading ? "Logging in…" : "Login"}
        </button>

        <p className="auth-switch">
          Don't have an account? <Link to="/signup">Sign up</Link>
        </p>
      </form>
    </AuthLayout>
  );
}