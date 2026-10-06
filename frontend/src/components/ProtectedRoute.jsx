import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function ProtectedRoute({ children }) {
  const { user } = useAuth();
  // If not logged in, redirect to /login
  if (!user && !token) {
    return <Navigate to="/login" replace />;
  }

  return children;
}