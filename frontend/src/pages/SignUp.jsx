import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthLayout from "../components/AuthLayout.jsx";
import Field from "../components/Field.jsx";

export default function SignUp() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) =>
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (form.password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    setLoading(true);
    try {
      // TODO: replace with your API call, e.g.
      // const res = await fetch("/api/auth/register", {
      //   method: "POST",
      //   headers: { "Content-Type": "application/json" },
      //   body: JSON.stringify(form),
      // });
      // if (!res.ok) throw new Error((await res.json()).message);
      console.log("signup", form);
      navigate("/login");
    } catch (err) {
      setError(err.message || "Could not create your account. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout>
      <form className="auth-form" onSubmit={handleSubmit}>
        <h1>Sign up</h1>
        <p className="auth-sub">Create your VaultQuery account.</p>

        <Field
          label="Name"
          name="name"
          placeholder="Your full name"
          autoComplete="name"
          value={form.name}
          onChange={handleChange}
          required
        />
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
          placeholder="At least 8 characters"
          autoComplete="new-password"
          minLength={8}
          value={form.password}
          onChange={handleChange}
          required
        />

        {error && <p className="auth-error" role="alert">{error}</p>}

        <button className="btn-primary" type="submit" disabled={loading}>
          {loading ? "Creating account…" : "Sign up"}
        </button>

        <p className="auth-switch">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </AuthLayout>
  );
}