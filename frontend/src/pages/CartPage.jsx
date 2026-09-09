import { Link, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { Trash2, Minus, Plus, ShoppingBag } from "lucide-react";
import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";
import api from "../lib/api";
import { Button } from "../components/ui/button";
import { useState } from "react";

export default function CartPage() {
  const { items, remove, setQty, total, clear } = useCart();
  const { user } = useAuth();
  const nav = useNavigate();
  const [loading, setLoading] = useState(false);

  const checkout = async () => {
    if (!user) { toast.error("Please login to checkout"); nav("/login"); return; }
    if (items.length === 0) return;
    setLoading(true);
    try {
      const { data } = await api.post("/api/payments/checkout", {
        items: items.map((i) => ({ product_id: i.product_id, quantity: i.quantity })),
        origin_url: window.location.origin,
      });
      window.location.href = data.checkout_url;
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Checkout failed");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <h1 className="font-display text-3xl sm:text-4xl font-bold tracking-tight">Your Cart</h1>
        <p className="text-slate-600 mt-2">{items.length} item{items.length !== 1 && "s"}</p>

        {items.length === 0 ? (
          <div className="mt-16 text-center border border-dashed border-slate-300 rounded-xl p-16">
            <ShoppingBag className="w-12 h-12 mx-auto text-slate-300" />
            <p className="mt-4 text-slate-600">Your cart is empty.</p>
            <Link to="/shops"><Button className="mt-4 bg-orange-700 hover:bg-orange-800 rounded-full">Browse Shops</Button></Link>
          </div>
        ) : (
          <div className="grid lg:grid-cols-3 gap-8 mt-8">
            <div className="lg:col-span-2 space-y-3">
              {items.map((i) => (
                <div key={i.product_id} data-testid={`cart-item-${i.product_id}`} className="bg-white border border-slate-200 rounded-xl p-4 flex gap-4">
                  <img src={i.image_url || "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=200"} alt={i.name} className="w-24 h-24 object-cover rounded-lg" />
                  <div className="flex-1">
                    <h4 className="font-display font-semibold">{i.name}</h4>
                    <p className="text-sm text-slate-600">₹{i.price.toLocaleString()}</p>
                    <div className="flex items-center gap-2 mt-3">
                      <button data-testid={`qty-dec-${i.product_id}`} onClick={() => setQty(i.product_id, i.quantity - 1)} className="w-7 h-7 rounded-full border border-slate-300 flex items-center justify-center"><Minus className="w-3 h-3" /></button>
                      <span className="w-8 text-center text-sm">{i.quantity}</span>
                      <button data-testid={`qty-inc-${i.product_id}`} onClick={() => setQty(i.product_id, i.quantity + 1)} className="w-7 h-7 rounded-full border border-slate-300 flex items-center justify-center"><Plus className="w-3 h-3" /></button>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-display font-bold">₹{(i.price * i.quantity).toLocaleString()}</div>
                    <button data-testid={`cart-remove-${i.product_id}`} onClick={() => remove(i.product_id)} className="mt-2 text-red-600 text-xs flex items-center gap-1"><Trash2 className="w-3 h-3" /> Remove</button>
                  </div>
                </div>
              ))}
            </div>
            <div className="bg-white border border-slate-200 rounded-xl p-6 h-fit sticky top-24">
              <h3 className="font-display text-xl font-bold">Order Summary</h3>
              <div className="mt-4 space-y-2 text-sm">
                <div className="flex justify-between"><span>Subtotal</span><span>₹{total.toLocaleString()}</span></div>
                <div className="flex justify-between"><span>Delivery</span><span className="text-emerald-700">Free</span></div>
                <div className="border-t border-slate-200 pt-3 flex justify-between font-display font-bold text-lg"><span>Total</span><span>₹{total.toLocaleString()}</span></div>
              </div>
              <Button data-testid="checkout-btn" disabled={loading} onClick={checkout} className="w-full mt-6 bg-orange-700 hover:bg-orange-800 rounded-full h-12">
                {loading ? "Redirecting..." : "Proceed to Checkout"}
              </Button>
              <button onClick={clear} className="w-full mt-2 text-xs text-slate-500 hover:text-red-600">Clear cart</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
