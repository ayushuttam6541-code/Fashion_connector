import { useState } from "react";
import { toast } from "sonner";
import { Mail, Phone, MapPin, MessageSquare } from "lucide-react";
import api from "../lib/api";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Label } from "../components/ui/label";

export default function ContactPage() {
  const [form, setForm] = useState({ name: "", email: "", phone: "", message: "" });
  const [loading, setLoading] = useState(false);
  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post("/contact", form);
      toast.success("Message sent! We'll get back within 24 hours.");
      setForm({ name: "", email: "", phone: "", message: "" });
    } catch (error) {
      console.error("Failed to send contact message:", error);
      console.error("Error response:", error?.response);
      console.error("Error message:", error?.message);
      toast.error(error?.response?.data?.detail || "Failed to send");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 grid lg:grid-cols-2 gap-12">
        <div>
          <h1 className="font-display text-4xl sm:text-5xl font-bold tracking-tight">Let's talk</h1>
          <p className="text-slate-600 mt-4 leading-relaxed">
            Questions about becoming a seller? Feedback on a shop? Need help with an order?
            We're a small team based in Patna and we reply fast.
          </p>
          <div className="mt-8 space-y-4">
            <div className="flex items-center gap-3"><div className="w-10 h-10 rounded-lg bg-orange-50 text-orange-700 flex items-center justify-center"><Mail className="w-5 h-5" /></div><div><div className="font-semibold">Email</div><div className="text-sm text-slate-600">kamalayush65@gmail.com</div></div></div>
            <div className="flex items-center gap-3"><div className="w-10 h-10 rounded-lg bg-orange-50 text-orange-700 flex items-center justify-center"><Phone className="w-5 h-5" /></div><div><div className="font-semibold">Phone</div><div className="text-sm text-slate-600">8709610659</div></div></div>
            <div className="flex items-center gap-3"><div className="w-10 h-10 rounded-lg bg-orange-50 text-orange-700 flex items-center justify-center"><MapPin className="w-5 h-5" /></div><div><div className="font-semibold">Office</div><div className="text-sm text-slate-600">Khemanichak Aadarsh Colony Road No 1, Patna, Bihar</div></div></div>
          </div>
        </div>
        <form onSubmit={submit} className="bg-slate-50 border border-slate-200 rounded-2xl p-8 space-y-4">
          <div className="flex items-center gap-2 mb-2"><MessageSquare className="w-5 h-5 text-orange-700" /><h2 className="font-display text-xl font-bold">Send a message</h2></div>
          <div><Label>Name</Label><Input data-testid="contact-name" required value={form.name} onChange={(e) => set("name", e.target.value)} /></div>
          <div><Label>Email</Label><Input data-testid="contact-email" type="email" required value={form.email} onChange={(e) => set("email", e.target.value)} /></div>
          <div><Label>Phone (optional)</Label><Input data-testid="contact-phone" value={form.phone} onChange={(e) => set("phone", e.target.value)} /></div>
          <div><Label>Message</Label><Textarea data-testid="contact-message" required rows={5} value={form.message} onChange={(e) => set("message", e.target.value)} /></div>
          <Button data-testid="contact-submit" type="submit" disabled={loading} className="w-full bg-orange-700 hover:bg-orange-800 rounded-full h-11">{loading ? "Sending..." : "Send Message"}</Button>
        </form>
      </div>
    </div>
  );
}
