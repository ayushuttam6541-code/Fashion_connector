import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";

export default function LoginPage() {
  const { login } = useAuth();
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await login(email, password);
      toast.success(`Welcome back, ${data.name}`);
      if (data.role === "admin") nav("/admin");
      else if (data.role === "seller") nav("/seller/dashboard");
      else nav("/");
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Login failed");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white border border-slate-200 rounded-2xl p-8">
        <h1 className="font-display text-3xl font-bold tracking-tight">Welcome back</h1>
        <p className="text-slate-600 mt-2 text-sm">Login to your FashionConnect account</p>
        <form onSubmit={submit} className="mt-8 space-y-4">
          <div>
            <Label>Email</Label>
            <Input data-testid="login-email" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div>
            <Label>Password</Label>
            <Input data-testid="login-password" type="password" required value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
          <Button data-testid="login-submit" type="submit" disabled={loading} className="w-full bg-slate-900 hover:bg-slate-800 rounded-full h-11">
            {loading ? "Logging in..." : "Login"}
          </Button>
        </form>
        <p className="text-center text-sm text-slate-600 mt-6">
          New to FashionConnect? <Link to="/register" className="text-orange-700 font-semibold hover:underline">Create account</Link>
        </p>
        <p className="text-center text-xs text-slate-400 mt-2">
          Are you a shopkeeper? <Link to="/sell" className="text-orange-700 hover:underline">Register your shop →</Link>
        </p>
      </div>
    </div>
  );
}
