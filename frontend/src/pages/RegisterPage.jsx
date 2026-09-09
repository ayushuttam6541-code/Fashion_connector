import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";

export default function RegisterPage() {
  const { register } = useAuth();
  const nav = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await register({ ...form, role: "customer" });
      toast.success("Account created!");
      nav("/");
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Registration failed");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white border border-slate-200 rounded-2xl p-8">
        <h1 className="font-display text-3xl font-bold tracking-tight">Create account</h1>
        <p className="text-slate-600 mt-2 text-sm">Shop from Patna's best clothing stores.</p>
        <form onSubmit={submit} className="mt-8 space-y-4">
          <div><Label>Name</Label><Input data-testid="signup-name" required value={form.name} onChange={(e) => set("name", e.target.value)} /></div>
          <div><Label>Email</Label><Input data-testid="signup-email" type="email" required value={form.email} onChange={(e) => set("email", e.target.value)} /></div>
          <div><Label>Password</Label><Input data-testid="signup-password" type="password" required minLength={6} value={form.password} onChange={(e) => set("password", e.target.value)} /></div>
          <Button data-testid="signup-submit" type="submit" disabled={loading} className="w-full bg-slate-900 hover:bg-slate-800 rounded-full h-11">
            {loading ? "Creating..." : "Create account"}
          </Button>
        </form>
        <p className="text-center text-sm text-slate-600 mt-6">
          Have an account? <Link to="/login" className="text-orange-700 font-semibold hover:underline">Login</Link>
        </p>
      </div>
    </div>
  );
}
