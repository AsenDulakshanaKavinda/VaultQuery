import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  console.log("Full User Object:", user);
  console.log("User Keys:", Object.keys(user || {}));

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <div className="auth-page">
      <div className="dash-frame">
        <header className="dash-header">
          <div className="dash-brand">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <rect x="3" y="3" width="18" height="18" rx="5" stroke="currentColor" strokeWidth="2.4" />
              <circle cx="12" cy="12" r="3" fill="currentColor" />
            </svg>
            <span>VaultQuery</span>
          </div>
          <button className="btn-outline" onClick={handleLogout}>
            Logout
          </button>
        </header>

        <main className="dash-main">
          <h1>Dashboard</h1>
          <section className="dash-card" aria-label="Account details">
            <div className="dash-avatar" aria-hidden="true">
              {user.name?.charAt(0).toUpperCase()}
              
            </div>
            <dl>
              <div>
                <dt>ID</dt>
                <dd>{user.user_id}</dd>
              </div>
              <div>
                <dt>Name</dt>
                <dd>{user.username}</dd>
              </div>
              <div>
                <dt>Email</dt>
                <dd>{user.email}</dd>
              </div>
              <div>
                <dt>Role</dt>
                <dd>{user.role}</dd>
              </div>
              <div>
                <dt>Organization</dt>
                <dd>{user.organization}</dd>
              </div>
              <div>
                <dt>Status</dt>
                <dd>{user.status}</dd>
              </div>
            </dl>
          </section>
        </main>
      </div>
    </div>
  );
}