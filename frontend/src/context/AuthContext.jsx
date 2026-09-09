import { createContext, useContext, useEffect, useState, useCallback } from "react";
import api from "../lib/api";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchMe = useCallback(async () => {
    const token = localStorage.getItem("fc_token");
    if (!token) { setLoading(false); return; }
    try {
      const { data } = await api.get("/auth/me");
      setUser(data);
    } catch { localStorage.removeItem("fc_token"); }
    setLoading(false);
  }, []);

  useEffect(() => { fetchMe(); }, [fetchMe]);

  const login = async (email, password) => {
    const { data } = await api.post("/auth/login", { email, password });
    localStorage.setItem("fc_token", data.token);
    setUser({ id: data.id, email: data.email, name: data.name, role: data.role });
    return data;
  };

  const register = async (payload) => {
    const { data } = await api.post("/auth/register", payload);
    localStorage.setItem("fc_token", data.token);
    setUser({ id: data.id, email: data.email, name: data.name, role: data.role });
    return data;
  };

  const logout = async () => {
    try { await api.post("/auth/logout"); } catch {}
    localStorage.removeItem("fc_token");
    setUser(null);
  };

  const setSession = (data) => {
    localStorage.setItem("fc_token", data.token);
    setUser({ id: data.id || data.owner_id, email: data.email || data.owner_email,
             name: data.name || data.owner_name, role: data.role || "seller" });
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, setSession, fetchMe }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
