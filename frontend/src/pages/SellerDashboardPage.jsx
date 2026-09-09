import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "sonner";
import { Store, Package, ShoppingBag, TrendingUp, Plus, Trash2, Edit } from "lucide-react";
import api from "../lib/api";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Label } from "../components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "../components/ui/dialog";

const CATEGORIES = ["Men's Fashion", "Women's Fashion", "Kids Wear", "Ethnic Wear", "Boutiques"];

function ProductForm({ onSave, initial }) {
  const [form, setForm] = useState(initial || { name: "", description: "", price: "", category: "Men", image_url: "", stock: 10 });
  const [uploading, setUploading] = useState(false);
  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  const upload = async (file) => {
    if (!file) return;
    setUploading(true);
    try {
      const fd = new FormData(); fd.append("file", file);
      const { data } = await api.post("/api/upload", fd, { headers: { "Content-Type": "multipart/form-data" }});
      set("image_url", `${process.env.REACT_APP_BACKEND_URL}${data.url}`);
      toast.success("Uploaded");
    } catch (e) { toast.error("Upload failed"); }
    setUploading(false);
  };

  return (
    <form onSubmit={(e) => { e.preventDefault(); onSave({ ...form, price: parseFloat(form.price), stock: parseInt(form.stock) || 0 }); }} className="space-y-4">
      <div><Label>Product Name</Label><Input data-testid="prod-name" required value={form.name} onChange={(e) => set("name", e.target.value)} /></div>
      <div><Label>Description</Label><Textarea data-testid="prod-desc" value={form.description} onChange={(e) => set("description", e.target.value)} /></div>
      <div className="grid grid-cols-2 gap-3">
        <div><Label>Price (₹)</Label><Input data-testid="prod-price" type="number" required min="0" step="1" value={form.price} onChange={(e) => set("price", e.target.value)} /></div>
        <div><Label>Stock</Label><Input data-testid="prod-stock" type="number" min="0" value={form.stock} onChange={(e) => set("stock", e.target.value)} /></div>
      </div>
      <div>
        <Label>Category</Label>
        <Select value={form.category} onValueChange={(v) => set("category", v)}>
          <SelectTrigger data-testid="prod-category"><SelectValue /></SelectTrigger>
          <SelectContent>{CATEGORIES.map((c) => <SelectItem key={c} value={c}>{c}</SelectItem>)}</SelectContent>
        </Select>
      </div>
      <div>
        <Label>Image</Label>
        <div className="border-2 border-dashed border-slate-300 rounded-xl p-3">
          {form.image_url && <img src={form.image_url} alt="" className="w-full h-32 object-cover rounded-lg mb-2" />}
          <input data-testid="prod-image" type="file" accept="image/*" onChange={(e) => upload(e.target.files?.[0])} disabled={uploading} className="text-xs" />
        </div>
      </div>
      <Button data-testid="prod-save" type="submit" className="w-full bg-orange-700 hover:bg-orange-800 rounded-full">Save Product</Button>
    </form>
  );
}

export default function SellerDashboardPage() {
  const [shop, setShop] = useState(null);
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState(null);

  const refresh = async () => {
    try {
      const { data: s } = await api.get("/shops/mine");
      setShop(s);
      if (s) {
        const [{ data: p }, { data: o }] = await Promise.all([
          api.get(`/api/products?shop_id=${s.id}`),
          api.get("/api/orders"),
        ]);
        setProducts(p);
        setOrders(o);
      }
    } catch {}
  };
  useEffect(() => { refresh(); }, []);

  const saveProduct = async (payload) => {
    try {
      if (editing) await api.put(`/products/${editing.id}`, payload);
      else await api.post("/api/products", payload);
      toast.success(editing ? "Product updated" : "Product added");
      setDialogOpen(false); setEditing(null);
      refresh();
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Save failed");
    }
  };

  const del = async (pid) => {
    if (!window.confirm("Delete this product?")) return;
    try { await api.delete(`/products/${pid}`); toast.success("Deleted"); refresh(); }
    catch (e) { toast.error("Delete failed"); }
  };

  if (!shop) return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center">
      <div className="text-center">
        <Store className="w-12 h-12 mx-auto text-slate-400" />
        <h2 className="font-display text-2xl font-bold mt-4">No shop yet</h2>
        <p className="text-slate-600 mt-2">Register your shop to start selling.</p>
        <Link to="/sell"><Button className="mt-4 bg-orange-700 hover:bg-orange-800 rounded-full">Register Shop</Button></Link>
      </div>
    </div>
  );

  const totalRevenue = orders.filter(o => o.payment_status === "paid").reduce((s, o) => s + (o.total || 0), 0);

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="mb-8 flex items-start justify-between gap-4 flex-wrap">
          <div>
            <p className="text-xs uppercase tracking-widest text-slate-500 font-semibold">Seller Dashboard</p>
            <h1 className="font-display text-3xl sm:text-4xl font-bold tracking-tight mt-1">{shop.name}</h1>
            <p className="text-sm text-slate-600 mt-1">{shop.verified ? "Verified seller" : "Pending verification"} · {shop.city}</p>
          </div>
          <Link to={`/shops/${shop.id}`}><Button variant="outline" className="rounded-full">View public page →</Button></Link>
        </div>

        <div className="grid sm:grid-cols-4 gap-4 mb-8">
          {[
            { icon: Package, label: "Products", val: products.length, color: "bg-blue-50 text-blue-700" },
            { icon: ShoppingBag, label: "Orders", val: orders.length, color: "bg-purple-50 text-purple-700" },
            { icon: TrendingUp, label: "Revenue", val: `₹${totalRevenue.toLocaleString()}`, color: "bg-emerald-50 text-emerald-700" },
            { icon: Store, label: "Rating", val: `${shop.rating?.toFixed(1) || "4.5"} ★`, color: "bg-amber-50 text-amber-700" },
          ].map((s) => (
            <div key={s.label} className="bg-white border border-slate-200 rounded-xl p-5">
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${s.color}`}><s.icon className="w-5 h-5" /></div>
              <div className="text-xs text-slate-500 mt-3">{s.label}</div>
              <div className="font-display text-2xl font-bold">{s.val}</div>
            </div>
          ))}
        </div>

        <Tabs defaultValue="products">
          <TabsList data-testid="dash-tabs">
            <TabsTrigger data-testid="tab-products" value="products">Products</TabsTrigger>
            <TabsTrigger data-testid="tab-orders" value="orders">Orders</TabsTrigger>
            <TabsTrigger data-testid="tab-shop" value="shop">Shop Info</TabsTrigger>
          </TabsList>
          <TabsContent value="products" className="mt-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-display text-xl font-bold">Your Products</h3>
              <Dialog open={dialogOpen} onOpenChange={(o) => { setDialogOpen(o); if (!o) setEditing(null); }}>
                <DialogTrigger asChild>
                  <Button data-testid="add-product-btn" className="bg-orange-700 hover:bg-orange-800 rounded-full"><Plus className="w-4 h-4 mr-1" /> Add Product</Button>
                </DialogTrigger>
                <DialogContent className="max-w-lg">
                  <DialogHeader><DialogTitle>{editing ? "Edit Product" : "Add Product"}</DialogTitle></DialogHeader>
                  <ProductForm onSave={saveProduct} initial={editing} />
                </DialogContent>
              </Dialog>
            </div>
            {products.length === 0 ? (
              <div className="text-center text-slate-500 py-20 border border-dashed rounded-xl">No products yet. Add your first product!</div>
            ) : (
              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {products.map((p) => (
                  <div key={p.id} className="bg-white border border-slate-200 rounded-xl overflow-hidden">
                    <img src={p.image_url || "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400"} className="w-full h-40 object-cover" alt="" />
                    <div className="p-4">
                      <h4 className="font-display font-semibold truncate">{p.name}</h4>
                      <div className="flex items-center justify-between mt-2">
                        <span className="font-bold">₹{p.price.toLocaleString()}</span>
                        <span className="text-xs text-slate-500">Stock: {p.stock}</span>
                      </div>
                      <div className="flex gap-2 mt-3">
                        <Button data-testid={`edit-${p.id}`} size="sm" variant="outline" className="flex-1" onClick={() => { setEditing(p); setDialogOpen(true); }}><Edit className="w-3 h-3" /></Button>
                        <Button data-testid={`del-${p.id}`} size="sm" variant="outline" className="text-red-600" onClick={() => del(p.id)}><Trash2 className="w-3 h-3" /></Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </TabsContent>
          <TabsContent value="orders" className="mt-6">
            <h3 className="font-display text-xl font-bold mb-4">Recent Orders</h3>
            {orders.length === 0 ? (
              <div className="text-center text-slate-500 py-20 border border-dashed rounded-xl">No orders yet.</div>
            ) : (
              <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
                <table className="w-full text-sm">
                  <thead className="bg-slate-50 text-left"><tr><th className="p-4">Order ID</th><th>Customer</th><th>Total</th><th>Status</th><th>Date</th></tr></thead>
                  <tbody>
                    {orders.map((o) => (
                      <tr key={o.id} className="border-t border-slate-200">
                        <td className="p-4 font-mono text-xs">{o.id.slice(0, 8)}</td>
                        <td>{o.customer_email}</td>
                        <td>₹{o.total?.toLocaleString()}</td>
                        <td><span className={`text-xs px-2 py-1 rounded-full ${o.payment_status === "paid" ? "bg-emerald-100 text-emerald-700" : "bg-amber-100 text-amber-700"}`}>{o.payment_status}</span></td>
                        <td className="text-slate-500">{new Date(o.created_at).toLocaleDateString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </TabsContent>
          <TabsContent value="shop" className="mt-6">
            <div className="bg-white border border-slate-200 rounded-xl p-6 space-y-2">
              <h3 className="font-display text-xl font-bold mb-3">Shop Details</h3>
              <p><b>Address:</b> {shop.address}</p>
              <p><b>Phone:</b> {shop.phone}</p>
              <p><b>Email:</b> {shop.email}</p>
              <p><b>Business Hours:</b> {shop.business_hours}</p>
              <p><b>Categories:</b> {shop.categories.join(", ")}</p>
              <p><b>Services:</b> {shop.services.join(", ")}</p>
              <p><b>Verified:</b> {shop.verified ? "Yes ✓" : "Pending"}</p>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
