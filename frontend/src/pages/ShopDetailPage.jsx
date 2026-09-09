import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { MapPin, Phone, Clock, ShieldCheck, Star, Navigation, ShoppingBag, Mail } from "lucide-react";
import { toast } from "sonner";
import api from "../lib/api";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { useCart } from "../context/CartContext";

export default function ShopDetailPage() {
  const { id } = useParams();
  const [shop, setShop] = useState(null);
  const { add } = useCart();

  useEffect(() => {
    api.get(`/shops/${id}`).then((r) => setShop(r.data)).catch(() => setShop(null));
  }, [id]);

  if (!shop) return <div className="min-h-screen flex items-center justify-center text-slate-500">Loading...</div>;

  const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(shop.address)}`;

  return (
    <div className="bg-white min-h-screen">
      <div className="relative h-64 sm:h-80 bg-slate-100 overflow-hidden">
        <img src={shop.banner_url || "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1600"} className="w-full h-full object-cover" alt={shop.name} />
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent" />
        <div className="absolute bottom-6 left-0 right-0 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
            <div className="text-white">
              <div className="flex items-center gap-2 mb-2">
                {shop.verified && <Badge className="bg-emerald-600 border-none gap-1"><ShieldCheck className="w-3 h-3" /> Verified</Badge>}
                <Badge variant="outline" className="bg-white/10 text-white border-white/30">{(shop.categories || []).join(" • ")}</Badge>
              </div>
              <h1 className="font-display text-3xl sm:text-5xl font-bold">{shop.name}</h1>
              <p className="text-white/80 mt-1 max-w-xl">{shop.description}</p>
            </div>
            <div className="flex gap-2">
              <a href={mapsUrl} target="_blank" rel="noopener noreferrer" data-testid="shop-map-btn">
                <Button className="bg-white text-slate-900 hover:bg-slate-100 rounded-full"><Navigation className="w-4 h-4 mr-2" /> Get Directions</Button>
              </a>
              <a href={`tel:${shop.phone}`} data-testid="shop-call-btn">
                <Button variant="outline" className="rounded-full bg-white/10 text-white border-white/30 hover:bg-white/20"><Phone className="w-4 h-4 mr-2" /> Call</Button>
              </a>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 grid lg:grid-cols-3 gap-10">
        <aside className="space-y-4">
          <div className="border border-slate-200 rounded-xl p-6">
            <h3 className="font-display font-bold text-lg mb-4">Shop Info</h3>
            <ul className="space-y-3 text-sm">
              <li className="flex items-start gap-2"><MapPin className="w-4 h-4 mt-0.5 text-slate-500" /><span>{shop.address}</span></li>
              <li className="flex items-center gap-2"><Phone className="w-4 h-4 text-slate-500" /><span>{shop.phone}</span></li>
              <li className="flex items-center gap-2"><Mail className="w-4 h-4 text-slate-500" /><span>{shop.email}</span></li>
              <li className="flex items-center gap-2"><Clock className="w-4 h-4 text-slate-500" /><span>{shop.business_hours}</span></li>
              <li className="flex items-center gap-2"><Star className="w-4 h-4 fill-amber-500 text-amber-500" /><span>{shop.rating?.toFixed(1)} ({shop.review_count} reviews)</span></li>
            </ul>
          </div>
          <div className="border border-slate-200 rounded-xl p-6">
            <h3 className="font-display font-bold text-lg mb-3">Services</h3>
            <div className="flex flex-wrap gap-2">
              {(shop.services || []).map((s) => (
                <span key={s} className="text-xs bg-slate-100 rounded-full px-3 py-1">{s}</span>
              ))}
            </div>
          </div>
        </aside>

        <div className="lg:col-span-2">
          <h2 className="font-display text-2xl font-bold mb-4">Products</h2>
          {(!shop.products || shop.products.length === 0) ? (
            <div className="text-slate-500 border border-dashed border-slate-300 rounded-xl p-10 text-center">This shop hasn't added any products yet.</div>
          ) : (
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {shop.products.map((p) => (
                <div key={p.id} data-testid={`product-${p.id}`} className="border border-slate-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow">
                  <div className="aspect-square bg-slate-100 overflow-hidden">
                    <img src={p.image_url || "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=600"} className="w-full h-full object-cover hover:scale-105 transition-transform duration-500" alt={p.name} />
                  </div>
                  <div className="p-4">
                    <h4 className="font-display font-semibold truncate">{p.name}</h4>
                    <p className="text-xs text-slate-500">{p.category}</p>
                    <div className="flex items-center justify-between mt-3">
                      <span className="font-display font-bold text-lg">₹{p.price.toLocaleString()}</span>
                      <Button
                        size="sm"
                        className="bg-orange-700 hover:bg-orange-800 rounded-full"
                        data-testid={`add-cart-${p.id}`}
                        onClick={() => { add(p); toast.success("Added to cart"); }}
                      >
                        <ShoppingBag className="w-3.5 h-3.5 mr-1" /> Add
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
