import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { Store, Upload, CheckCircle2 } from "lucide-react";
import api from "../lib/api";
import { useAuth } from "../context/AuthContext";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Label } from "../components/ui/label";
import { Checkbox } from "../components/ui/checkbox";

const CATEGORIES = ["Men", "Women", "Kids", "Ethnic Wear", "Boutiques"];

export default function SellerRegisterPage() {
  const { user, setSession } = useAuth();
  const nav = useNavigate();
  const [form, setForm] = useState({
    name: "", owner_name: user?.name || "", phone: "",
    email: user?.email || "", password: "",
    address: "", city: "Patna", gst: "",
    business_hours: "10:00 AM - 09:00 PM", description: "",
    categories: [], services: "",
    logo_url: "", banner_url: "",
  });
  const [submitting, setSubmitting] = useState(false);
  const [uploading, setUploading] = useState({ logo: false, banner: false });

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  const toggleCat = (c) => {
    setForm((f) => ({
      ...f, categories: f.categories.includes(c)
        ? f.categories.filter((x) => x !== c) : [...f.categories, c],
    }));
  };

  const handleUpload = async (kind, file) => {
    if (!file) return;
    if (!user) {
      toast.error("Please login or set a password below before uploading. Uploads require an account.");
      return;
    }
    setUploading((u) => ({ ...u, [kind]: true }));
    try {
      const fd = new FormData();
      fd.append("file", file);
      const { data } = await api.post("/api/upload", fd, { headers: { "Content-Type": "multipart/form-data" }});
      const fullUrl = `${process.env.REACT_APP_BACKEND_URL}${data.url}`;
      set(kind === "logo" ? "logo_url" : "banner_url", fullUrl);
      toast.success(`${kind} uploaded`);
    } catch (e) {
      toast.error(`Upload failed: ${e?.response?.data?.detail || e.message}`);
    }
    setUploading((u) => ({ ...u, [kind]: false }));
  };

  const submit = async (e) => {
    e.preventDefault();
    if (form.categories.length === 0) { toast.error("Select at least one category"); return; }
    if (!user && !form.password) { toast.error("Set a password to create your seller account"); return; }
    setSubmitting(true);
    try {
      const payload = {
        ...form,
        services: form.services.split(",").map(s => s.trim()).filter(Boolean),
      };
      const { data } = await api.post("/api/shops", payload);
      if (data.token) setSession(data);
      toast.success("Shop registered! Redirecting to your dashboard...");
      setTimeout(() => nav("/seller/dashboard"), 800);
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Registration failed");
    }
    setSubmitting(false);
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 text-xs uppercase tracking-widest font-semibold text-orange-700 bg-orange-50 border border-orange-200 rounded-full px-3 py-1">
            <Store className="w-3 h-3" /> Seller Registration
          </div>
          <h1 className="font-display text-4xl sm:text-5xl font-bold tracking-tight mt-4">Register Your Shop</h1>
          <p className="text-slate-600 mt-3 max-w-lg mx-auto">Get your clothing store online in under 5 minutes. Free forever.</p>
        </div>

        <form onSubmit={submit} className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-10 space-y-6">
          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <Label>Shop Name *</Label>
              <Input data-testid="reg-name" required value={form.name} onChange={(e) => set("name", e.target.value)} placeholder="e.g. Fashion Hub" />
            </div>
            <div>
              <Label>Owner Name *</Label>
              <Input data-testid="reg-owner" required value={form.owner_name} onChange={(e) => set("owner_name", e.target.value)} />
            </div>
            <div>
              <Label>Mobile Number *</Label>
              <Input data-testid="reg-phone" required value={form.phone} onChange={(e) => set("phone", e.target.value)} placeholder="10-digit mobile" />
            </div>
            <div>
              <Label>Email *</Label>
              <Input data-testid="reg-email" type="email" required value={form.email} onChange={(e) => set("email", e.target.value)} disabled={!!user} />
            </div>
            {!user && (
              <div className="sm:col-span-2">
                <Label>Create Password *</Label>
                <Input data-testid="reg-password" type="password" required minLength={6} value={form.password} onChange={(e) => set("password", e.target.value)} placeholder="Min 6 characters" />
              </div>
            )}
            <div className="sm:col-span-2">
              <Label>Shop Address *</Label>
              <Textarea data-testid="reg-address" required value={form.address} onChange={(e) => set("address", e.target.value)} placeholder="Full address including landmark, city, pincode" />
            </div>
            <div>
              <Label>City *</Label>
              <Input data-testid="reg-city" required value={form.city} onChange={(e) => set("city", e.target.value)} />
            </div>
            <div>
              <Label>GST Number (Optional)</Label>
              <Input data-testid="reg-gst" value={form.gst} onChange={(e) => set("gst", e.target.value)} placeholder="15-digit GSTIN" />
            </div>
            <div className="sm:col-span-2">
              <Label>Business Hours</Label>
              <Input data-testid="reg-hours" value={form.business_hours} onChange={(e) => set("business_hours", e.target.value)} />
            </div>
            <div className="sm:col-span-2">
              <Label>Shop Description</Label>
              <Textarea data-testid="reg-desc" value={form.description} onChange={(e) => set("description", e.target.value)} placeholder="Tell customers what makes your shop special..." />
            </div>
            <div className="sm:col-span-2">
              <Label>Services (comma-separated)</Label>
              <Input data-testid="reg-services" value={form.services} onChange={(e) => set("services", e.target.value)} placeholder="e.g. Kurtas, Sarees, Custom Tailoring" />
            </div>
          </div>

          <div>
            <Label>Categories *</Label>
            <div className="flex flex-wrap gap-3 mt-2">
              {CATEGORIES.map((c) => (
                <label key={c} className="flex items-center gap-2 border border-slate-200 rounded-full px-4 py-2 cursor-pointer hover:border-orange-700">
                  <Checkbox data-testid={`reg-cat-${c}`} checked={form.categories.includes(c)} onCheckedChange={() => toggleCat(c)} />
                  <span className="text-sm">{c}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <Label>Shop Logo</Label>
              <div className="mt-2 border-2 border-dashed border-slate-300 rounded-xl p-4 hover:border-orange-700 transition-colors">
                {form.logo_url ? (
                  <img src={form.logo_url} alt="Logo" className="w-full h-32 object-cover rounded-lg" />
                ) : (
                  <div className="text-center text-slate-500 py-6">
                    <Upload className="w-6 h-6 mx-auto mb-1" />
                    <div className="text-xs">PNG, JPG up to 5MB</div>
                  </div>
                )}
                <input data-testid="reg-logo-upload" type="file" accept="image/*" className="mt-2 text-xs" onChange={(e) => handleUpload("logo", e.target.files?.[0])} disabled={uploading.logo} />
              </div>
            </div>
            <div>
              <Label>Shop Banner</Label>
              <div className="mt-2 border-2 border-dashed border-slate-300 rounded-xl p-4 hover:border-orange-700 transition-colors">
                {form.banner_url ? (
                  <img src={form.banner_url} alt="Banner" className="w-full h-32 object-cover rounded-lg" />
                ) : (
                  <div className="text-center text-slate-500 py-6">
                    <Upload className="w-6 h-6 mx-auto mb-1" />
                    <div className="text-xs">Wide banner (16:9 recommended)</div>
                  </div>
                )}
                <input data-testid="reg-banner-upload" type="file" accept="image/*" className="mt-2 text-xs" onChange={(e) => handleUpload("banner", e.target.files?.[0])} disabled={uploading.banner} />
              </div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 pt-4">
            <Button data-testid="reg-submit" type="submit" size="lg" disabled={submitting} className="bg-orange-700 hover:bg-orange-800 rounded-full h-12 px-8 flex-1">
              {submitting ? "Registering..." : (<><CheckCircle2 className="w-4 h-4 mr-2" /> Register My Shop</>)}
            </Button>
            <Link to="/login" className="text-sm text-slate-600 self-center hover:text-orange-700">Already a seller? Login →</Link>
          </div>
        </form>
      </div>
    </div>
  );
}
