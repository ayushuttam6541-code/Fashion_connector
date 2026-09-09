import { useEffect, useState, useCallback } from "react";
import { useSearchParams } from "react-router-dom";
import { Search, SlidersHorizontal } from "lucide-react";
import api from "../lib/api";
import ShopCard from "../components/ShopCard";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";

const CATEGORIES = ["All", "Men's Fashion", "Women's Fashion", "Kids Wear", "Ethnic Wear", "Boutiques"];

export default function ShopsPage() {
  const [params, setParams] = useSearchParams();
  const [shops, setShops] = useState([]);
  const [loading, setLoading] = useState(true);
  const [q, setQ] = useState(params.get("q") || "");
  const category = params.get("category") || "All";

  const fetchShops = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await api.get("/shops", { params: {
        category: category === "All" ? undefined : category,
        q: q || undefined,
      }});
      setShops(data);
    } catch (error) {
      console.error("Failed to fetch shops:", error);
      console.error("Error response:", error?.response);
      console.error("Error message:", error?.message);
    }
    setLoading(false);
  }, [category, q]);

  useEffect(() => { fetchShops(); }, [fetchShops]);

  const submit = (e) => {
    e.preventDefault();
    const p = new URLSearchParams(params);
    if (q) p.set("q", q); else p.delete("q");
    setParams(p);
    fetchShops();
  };

  const setCategory = (c) => {
    const p = new URLSearchParams(params);
    if (c === "All") p.delete("category"); else p.set("category", c);
    setParams(p);
  };

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="mb-8">
          <h1 className="font-display text-3xl sm:text-5xl font-bold tracking-tight">Discover Shops</h1>
          <p className="text-slate-600 mt-2">Browse {shops.length}+ trusted clothing shops across Patna.</p>
        </div>

        <form onSubmit={submit} className="flex flex-col sm:flex-row gap-3 mb-6">
          <div className="flex-1 relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2" />
            <Input
              data-testid="shops-search-input"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search shop name, address, service..."
              className="pl-11 h-12 rounded-full border-slate-300"
            />
          </div>
          <Button data-testid="shops-search-btn" type="submit" className="bg-slate-900 hover:bg-slate-800 rounded-full h-12 px-6">
            <SlidersHorizontal className="w-4 h-4 mr-2" /> Search
          </Button>
        </form>

        <div className="flex flex-wrap gap-2 mb-10">
          {CATEGORIES.map((c) => (
            <button
              key={c}
              data-testid={`filter-${c}`}
              onClick={() => setCategory(c)}
              className={`px-4 py-2 rounded-full text-sm font-medium border transition-colors ${
                category === c ? "bg-slate-900 text-white border-slate-900" : "bg-white text-slate-700 border-slate-300 hover:border-slate-900"
              }`}
            >{c}</button>
          ))}
        </div>

        {loading ? (
          <div className="text-slate-500 py-20 text-center">Loading shops...</div>
        ) : shops.length === 0 ? (
          <div className="text-slate-500 py-20 text-center" data-testid="shops-empty">No shops found. Try a different search.</div>
        ) : (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {shops.map((s, i) => <ShopCard key={s.id} shop={s} index={i} />)}
          </div>
        )}
      </div>
    </div>
  );
}
