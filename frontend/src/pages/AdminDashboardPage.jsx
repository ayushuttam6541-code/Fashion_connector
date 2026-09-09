import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Store, Users, Package, ShoppingBag, TrendingUp, ShieldCheck, Trash2, MessageSquare, Mail, Phone, Check, Archive } from "lucide-react";
import api from "../lib/api";
import { Button } from "../components/ui/button";

export default function AdminDashboardPage() {
  const [stats, setStats] = useState(null);
  const [shops, setShops] = useState([]);
  const [contactMessages, setContactMessages] = useState([]);
  const [activeTab, setActiveTab] = useState("overview");

  const refresh = async () => {
    try {
      const [{ data: s }, { data: sh }, { data: cm }] = await Promise.all([
        api.get("/admin/stats"),
        api.get("/admin/shops"),
        api.get("/admin/contact-messages")
      ]);
      setStats(s);
      setShops(sh);
      setContactMessages(cm);
    } catch (e) { toast.error("Failed to load admin data"); }
  };
  useEffect(() => { refresh(); }, []);

  const verify = async (id, on) => {
    try {
      await api.post(`/admin/shops/${id}/${on ? "verify" : "unverify"}`);
      toast.success(on ? "Verified" : "Unverified");
      refresh();
    } catch { toast.error("Action failed"); }
  };

  const del = async (id) => {
    if (!window.confirm("Delete this shop and all its products?")) return;
    try { await api.delete(`/admin/shops/${id}`); toast.success("Deleted"); refresh(); }
    catch { toast.error("Failed"); }
  };

  const updateMessageStatus = async (messageId, newStatus) => {
    try {
      await api.put(`/admin/contact-messages/${messageId}`, { status: newStatus });
      toast.success("Message status updated");
      refresh();
    } catch (error) {
      toast.error("Failed to update message status");
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <p className="text-xs uppercase tracking-widest text-orange-700 font-semibold">Admin</p>
        <h1 className="font-display text-3xl sm:text-4xl font-bold tracking-tight mt-1">Platform Overview</h1>

        {/* Tab Navigation */}
        <div className="flex gap-2 mt-6 border-b border-slate-200">
          <button
            onClick={() => setActiveTab("overview")}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === "overview" ? "border-orange-700 text-orange-700" : "border-transparent text-slate-600 hover:text-slate-900"
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab("messages")}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === "messages" ? "border-orange-700 text-orange-700" : "border-transparent text-slate-600 hover:text-slate-900"
            }`}
          >
            Contact Messages {stats?.new_contact_messages > 0 && (
              <span className="ml-2 bg-orange-700 text-white text-xs px-2 py-0.5 rounded-full">
                {stats.new_contact_messages}
              </span>
            )}
          </button>
        </div>

        {activeTab === "overview" && (
          <>
            {stats && (
              <div className="grid sm:grid-cols-3 lg:grid-cols-6 gap-4 mt-8">
                {[
                  { icon: Store, label: "Shops", val: stats.shops },
                  { icon: ShieldCheck, label: "Verified", val: stats.verified_shops },
                  { icon: Package, label: "Products", val: stats.products },
                  { icon: ShoppingBag, label: "Orders", val: stats.orders },
                  { icon: Users, label: "Users", val: stats.users },
                  { icon: TrendingUp, label: "Revenue", val: `₹${(stats.revenue || 0).toLocaleString()}` },
                ].map((s) => (
                  <div key={s.label} className="bg-white border border-slate-200 rounded-xl p-4">
                    <s.icon className="w-5 h-5 text-orange-700" />
                    <div className="text-xs text-slate-500 mt-2">{s.label}</div>
                    <div className="font-display text-xl font-bold">{s.val}</div>
                  </div>
                ))}
              </div>
            )}

            <h2 className="font-display text-2xl font-bold mt-10 mb-4">All Shops</h2>
            <div className="bg-white border border-slate-200 rounded-xl overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-slate-50 text-left">
                  <tr><th className="p-4">Shop</th><th>Owner</th><th>City</th><th>Categories</th><th>Verified</th><th>Actions</th></tr>
                </thead>
                <tbody>
                  {shops.map((s) => (
                    <tr key={s.id} className="border-t border-slate-200">
                      <td className="p-4"><div className="font-semibold">{s.name}</div><div className="text-xs text-slate-500">{s.phone}</div></td>
                      <td>{s.owner_name}<div className="text-xs text-slate-500">{s.email}</div></td>
                      <td>{s.short_address || s.city}</td>
                      <td className="text-xs">{s.category || s.categories?.join(", ")}</td>
                      <td>{s.verified ? <span className="text-emerald-700 text-xs font-semibold">Yes</span> : <span className="text-amber-700 text-xs font-semibold">No</span>}</td>
                      <td className="space-x-2">
                        {s.verified ? (
                          <Button data-testid={`admin-unverify-${s.id}`} size="sm" variant="outline" onClick={() => verify(s.id, false)}>Unverify</Button>
                        ) : (
                          <Button data-testid={`admin-verify-${s.id}`} size="sm" className="bg-emerald-600 hover:bg-emerald-700" onClick={() => verify(s.id, true)}><ShieldCheck className="w-3 h-3 mr-1" /> Verify</Button>
                        )}
                        <Button data-testid={`admin-del-${s.id}`} size="sm" variant="outline" className="text-red-600" onClick={() => del(s.id)}><Trash2 className="w-3 h-3" /></Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}

        {activeTab === "messages" && (
          <div className="mt-8">
            <h2 className="font-display text-2xl font-bold mb-4">Contact Messages</h2>
            <div className="bg-white border border-slate-200 rounded-xl overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-slate-50 text-left">
                  <tr><th className="p-4">Name</th><th>Email</th><th>Phone</th><th>Message</th><th>Status</th><th>Date</th><th>Actions</th></tr>
                </thead>
                <tbody>
                  {contactMessages.length === 0 ? (
                    <tr><td colSpan="7" className="p-8 text-center text-slate-500">No contact messages yet</td></tr>
                  ) : (
                    contactMessages.map((msg) => (
                      <tr key={msg.id} className="border-t border-slate-200">
                        <td className="p-4 font-semibold">{msg.name}</td>
                        <td className="p-4">
                          <div className="flex items-center gap-2">
                            <Mail className="w-4 h-4 text-slate-400" />
                            {msg.email}
                          </div>
                        </td>
                        <td className="p-4">
                          {msg.phone && (
                            <div className="flex items-center gap-2">
                              <Phone className="w-4 h-4 text-slate-400" />
                              {msg.phone}
                            </div>
                          )}
                        </td>
                        <td className="p-4 max-w-xs truncate">{msg.message}</td>
                        <td className="p-4">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                            msg.status === "new" ? "bg-orange-100 text-orange-700" :
                            msg.status === "read" ? "bg-blue-100 text-blue-700" :
                            msg.status === "replied" ? "bg-green-100 text-green-700" :
                            "bg-slate-100 text-slate-700"
                          }`}>
                            {msg.status}
                          </span>
                        </td>
                        <td className="p-4 text-xs text-slate-500">
                          {new Date(msg.created_at).toLocaleDateString()}
                        </td>
                        <td className="p-4 space-x-2">
                          {msg.status === "new" && (
                            <Button size="sm" variant="outline" onClick={() => updateMessageStatus(msg.id, "read")}>
                              <Check className="w-3 h-3 mr-1" /> Mark Read
                            </Button>
                          )}
                          {msg.status !== "archived" && (
                            <Button size="sm" variant="outline" onClick={() => updateMessageStatus(msg.id, "archived")}>
                              <Archive className="w-3 h-3 mr-1" /> Archive
                            </Button>
                          )}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
