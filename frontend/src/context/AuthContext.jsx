

import { createContext, useContext, useState, useEffect } from "react";

const AuthContext = createContext(null);
const USER_KEY = "vaultquery_user";
const TOKEN_KEY = "vaultquery_token";

function loadInitialState() {
  try {
    const user = JSON.parse(localStorage.getItem(USER_KEY));
    const token = localStorage.getItem(TOKEN_KEY);
    return { user, token };
  } catch {
    return { user: null, token: null };
  }
}

export function AuthProvider({ children }) {
  const [auth, setAuth] = useState(loadInitialState);

  // Background token validation on initial mount
  useEffect(() => {
    const verifyToken = async () => {
      const token = localStorage.getItem(TOKEN_KEY);
      if (!token) return;

      try {
        const response = await fetch("http://localhost:8080/api/v1/auth/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          // Update cached user details if server data changed
          localStorage.setItem(USER_KEY, JSON.stringify(data.user));
          setAuth((prev) => ({ ...prev, user: data.user }));
        } else {
          // Token expired or invalid — log out automatically
          logout();
        }
      } catch (err) {
        console.error("Failed to verify authentication session:", err);
      }
    };

    verifyToken();
  }, []);

  const login = (token, userData) => {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(userData));
    setAuth({ token, user: userData });
  };

  const logout = () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    setAuth({ token: null, user: null });
  };

  return (
    <AuthContext.Provider
      value={{
        user: auth.user,
        token: auth.token,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);