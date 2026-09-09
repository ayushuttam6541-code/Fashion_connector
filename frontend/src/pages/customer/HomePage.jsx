import { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowRight, Store, Package, TrendingUp, MapPin, CreditCard,
  LayoutDashboard, LineChart, BadgeCheck, Zap, Users, Headphones,
  Navigation, Search, ShoppingBag
} from "lucide-react";
import api from "../../lib/api";
import { Button } from "../../components/ui/button";
import ShopCard from "../../components/ShopCard";
import { useLocation } from "../../context/LocationContext";
import { toast } from "sonner";

const CATEGORIES = [
  { name: "Men's Fashion", img: "https://images.unsplash.com/photo-1617662408044-cda3ab7134c9?w=600" },
  { name: "Women's Fashion", img: "https://images.unsplash.com/photo-1567401893414-76b7b1e5a7a5?w=600" },
  { name: "Kids Wear", img: "https://images.unsplash.com/photo-1622218286192-95f6a20083c7?w=600" },
  { name: "Ethnic Wear", img: "https://images.pexels.com/photos/31427481/pexels-photo-31427481.jpeg?w=600" },
  { name: "Boutiques", img: "https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=600" },
];

const BENEFITS = [
  { icon: Zap, title: "No setup cost", desc: "Register and go live in minutes. Zero upfront fees." },
  { icon: Package, title: "Easy product upload", desc: "Add photos, prices and stock from your phone." },
  { icon: TrendingUp, title: "Instant online orders", desc: "Receive orders from customers across Patna." },
  { icon: MapPin, title: "Increased local visibility", desc: "Ranked on our featured shops and category pages." },
  { icon: LayoutDashboard, title: "Dedicated dashboard", desc: "Manage products, orders and earnings in one place." },
  { icon: CreditCard, title: "Secure payments", desc: "Direct settlement via Stripe. Safe & fast." },
  { icon: LineChart, title: "Analytics & reports", desc: "Track views, orders and top-selling products." },
  { icon: Users, title: "Inventory management", desc: "Real-time stock so you never oversell." },
];

const TRUST = [
  { icon: BadgeCheck, title: "Verified Sellers", desc: "Every shop is vetted before going live." },
  { icon: CreditCard, title: "Secure Payments", desc: "Bank-grade encryption on all transactions." },
  { icon: Headphones, title: "Fast Support", desc: "Priority chat & call support for shopkeepers." },
  { icon: Store, title: "Local Business First", desc: "We amplify Patna's local shopkeepers." },
];

export default function HomePage() {
  const [featured, setFeatured] = useState([]);
  const [nearbyShops, setNearbyShops] = useState([]);
  const [nearbyProducts, setNearbyProducts] = useState([]);
  
  const { location, requestLocation, formatDistance, isShopOpen } = useLocation();

  const loadFeaturedShops = useCallback(async () => {
    try {
      const { data } = await api.get("/shops/featured");
      setFeatured(data);
    } catch (error) {
      console.error("Failed to load featured shops:", error);
    }
  }, []);

  const loadNearbyContent = useCallback(async () => {
    if (!location) return;

    try {
      // Load nearby shops
      const { data: shops } = await api.get("/shops/nearby", {
        params: {
          latitude: location.latitude,
          longitude: location.longitude,
          max_distance: 5
        }
      });
      setNearbyShops(shops);

      // Load nearby products
      const { data: products } = await api.get("/api/products/nearby", {
        params: {
          latitude: location.latitude,
          longitude: location.longitude,
          max_distance: 5,
          limit: 8
        }
      });
      setNearbyProducts(products);
    } catch (error) {
      console.error("Failed to load nearby content:", error);
    }
  }, [location]);

  useEffect(() => {
    loadFeaturedShops();
  }, [loadFeaturedShops]);

  useEffect(() => {
    if (location) {
      loadNearbyContent();
    }
  }, [location, loadNearbyContent]);

  const handleUseLocation = async () => {
    try {
      await requestLocation();
      toast.success("Finding shops near you...");
    } catch (error) {
      toast.error("Could not access your location");
    }
  };

  return (
    <div className="bg-white">
      {/* HERO */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 -z-10">
          <img src="https://images.unsplash.com/photo-1621261027519-a71ac66d5a68?w=1600" className="w-full h-full object-cover opacity-20" alt="" />
          <div className="absolute inset-0 bg-gradient-to-b from-white via-white/90 to-white" />
        </div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-28 grid lg:grid-cols-12 gap-10 items-center">
          <div className="lg:col-span-7">
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
              <span className="inline-flex items-center gap-2 text-xs uppercase tracking-wider font-semibold text-orange-700 bg-orange-50 border border-orange-200 rounded-full px-3 py-1">
                <span className="w-1.5 h-1.5 rounded-full bg-orange-700 animate-pulse" /> Now onboarding shopkeepers in Patna
              </span>
              <h1 className="mt-6 font-display text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-[1.05]">
                Find Fashion <span className="text-orange-700">Near You</span>
              </h1>
              <p className="mt-6 text-lg text-slate-600 max-w-xl leading-relaxed">
                Discover clothes, ethnic wear, kids wear and more from shops around you in Patna.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                <Button 
                  size="lg" 
                  className="bg-orange-700 hover:bg-orange-800 rounded-full h-12 px-6"
                  onClick={handleUseLocation}
                >
                  <Navigation className="w-4 h-4 mr-2" />
                  Use My Location
                </Button>
                <Link to="/shops">
                  <Button size="lg" variant="outline" className="rounded-full h-12 px-6 border-slate-300">
                    <Search className="w-4 h-4 mr-2" />
                    Search Products
                  </Button>
                </Link>
              </div>
              {location && (
                <div className="mt-4 text-sm text-emerald-600 font-medium">
                  📍 Location enabled - showing nearby shops
                </div>
              )}
              <div className="mt-10 flex items-center gap-8 text-sm text-slate-500">
                <div><span className="font-display font-bold text-2xl text-slate-900">500+</span><br />Shops onboarded</div>
                <div><span className="font-display font-bold text-2xl text-slate-900">12k+</span><br />Products listed</div>
                <div><span className="font-display font-bold text-2xl text-slate-900">4.8★</span><br />Seller rating</div>
              </div>
            </motion.div>
          </div>
          <div className="lg:col-span-5 relative">
            <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.6, delay: 0.2 }} className="relative">
              <img src="https://images.unsplash.com/photo-1695391396401-5fbb4bedafc1?w=800" alt="Shopkeeper" className="w-full h-[520px] object-cover rounded-2xl shadow-xl" />
              <div className="absolute -bottom-6 -left-6 bg-white rounded-xl border border-slate-200 shadow-lg p-4 w-64">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center"><TrendingUp className="w-5 h-5 text-emerald-700" /></div>
                  <div>
                    <div className="text-xs text-slate-500">This month</div>
                    <div className="font-display font-bold text-lg">₹2,84,500</div>
                    <div className="text-xs text-emerald-600 font-medium">+23% vs last month</div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* NEARBY SHOPS */}
      {location && nearbyShops.length > 0 && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="flex items-end justify-between mb-8">
            <div>
              <h2 className="font-display text-3xl sm:text-4xl font-bold tracking-tight">Shops Near You</h2>
              <p className="text-slate-600 mt-2">Discover local fashion stores within 5 km</p>
            </div>
            <Link to="/shops" className="text-sm font-semibold text-orange-700 hover:underline">View all →</Link>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {nearbyShops.slice(0, 8).map((shop, i) => (
              <ShopCard 
                key={shop.id} 
                shop={shop} 
                index={i}
                distance={formatDistance(shop.distance)}
                isOpen={isShopOpen(shop.timings)}
              />
            ))}
          </div>
        </section>
      )}

      {/* NEARBY PRODUCTS */}
      {location && nearbyProducts.length > 0 && (
        <section className="bg-slate-50 border-y border-slate-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
            <div className="flex items-end justify-between mb-8">
              <div>
                <h2 className="font-display text-3xl sm:text-4xl font-bold tracking-tight">Products Near You</h2>
                <p className="text-slate-600 mt-2">Available products from nearby shops</p>
              </div>
              <Link to="/shops" className="text-sm font-semibold text-orange-700 hover:underline">View all →</Link>
            </div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {nearbyProducts.slice(0, 8).map((product) => (
                <Link key={product.id} to={`/products/${product.id}`} className="group">
                  <div className="bg-white border border-slate-200 rounded-xl overflow-hidden hover:shadow-lg transition-shadow">
                    <div className="relative">
                      <img 
                        src={product.images?.[0] || "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400"} 
                        alt={product.name} 
                        className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300" 
                      />
                      {product.distance && (
                        <div className="absolute top-2 right-2 bg-white/90 backdrop-blur-sm rounded-full px-2 py-1 text-xs font-medium text-slate-700">
                          {formatDistance(product.distance)}
                        </div>
                      )}
                    </div>
                    <div className="p-4">
                      <h3 className="font-display font-semibold text-sm truncate">{product.name}</h3>
                      <p className="text-xs text-slate-500 mt-1">{product.shop_name}</p>
                      <div className="flex items-center justify-between mt-2">
                        <span className="font-bold text-orange-700">
                          ₹{product.discount_price || product.price}
                        </span>
                        {product.discount_price && (
                          <span className="text-xs text-slate-400 line-through">₹{product.price}</span>
                        )}
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CATEGORIES */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="flex items-end justify-between mb-8">
          <div>
            <h2 className="font-display text-3xl sm:text-4xl font-bold tracking-tight">Shop by Category</h2>
            <p className="text-slate-600 mt-2">Curated collections from Patna's finest shops.</p>
          </div>
          <Link to="/shops" className="text-sm font-semibold text-orange-700 hover:underline hidden sm:inline">View all →</Link>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {CATEGORIES.map((c) => (
            <Link key={c.name} to={`/shops?category=${encodeURIComponent(c.name)}`} className="group relative overflow-hidden rounded-xl aspect-[3/4] border border-slate-200">
              <img src={c.img} alt={c.name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
              <div className="absolute bottom-4 left-4 right-4 text-white">
                <div className="font-display font-bold text-lg">{c.name}</div>
                <div className="text-xs opacity-80 group-hover:opacity-100">Explore shops →</div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* FEATURED SHOPS */}
      <section className="bg-slate-50 border-y border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="flex items-end justify-between mb-8">
            <div>
              <h2 className="font-display text-3xl sm:text-4xl font-bold tracking-tight">Featured Shops</h2>
              <p className="text-slate-600 mt-2">Hand-picked, verified sellers loved by shoppers.</p>
            </div>
            <Link to="/shops" className="text-sm font-semibold text-orange-700 hover:underline">View all →</Link>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {featured.slice(0, 8).map((s, i) => <ShopCard key={s.id} shop={s} index={i} />)}
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <span className="text-xs uppercase tracking-widest font-semibold text-orange-700">How It Works</span>
          <h2 className="font-display text-3xl sm:text-4xl font-bold tracking-tight mt-3">Find Fashion Near You in 4 Steps</h2>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {[
            { step: "1", title: "Share Location", desc: "Allow GPS access to find shops near you", icon: Navigation },
            { step: "2", title: "Discover Shops", desc: "Browse verified local clothing stores", icon: Store },
            { step: "3", title: "Find Products", desc: "Search available items with real-time stock", icon: Package },
            { step: "4", title: "Order or Pickup", desc: "Place order or visit the store directly", icon: ShoppingBag }
          ].map((item) => (
            <div key={item.step} className="text-center">
              <div className="w-16 h-16 rounded-full bg-orange-100 text-orange-700 flex items-center justify-center mx-auto mb-4">
                <item.icon className="w-8 h-8" />
              </div>
              <div className="text-xs font-bold text-orange-700 mb-2">STEP {item.step}</div>
              <h3 className="font-display font-bold text-lg mb-2">{item.title}</h3>
              <p className="text-sm text-slate-600">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* BENEFITS */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <span className="text-xs uppercase tracking-widest font-semibold text-orange-700">Why FashionConnect</span>
          <h2 className="font-display text-3xl sm:text-4xl font-bold tracking-tight mt-3">Everything you need to grow online</h2>
          <p className="text-slate-600 mt-3">Built for local shopkeepers — no tech skills required.</p>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {BENEFITS.map((b) => (
            <div key={b.title} className="p-6 border border-slate-200 rounded-xl hover:border-orange-700 hover:shadow-md transition-[border-color,box-shadow]">
              <div className="w-11 h-11 rounded-lg bg-orange-50 text-orange-700 flex items-center justify-center mb-4"><b.icon className="w-5 h-5" /></div>
              <h3 className="font-display font-bold text-base">{b.title}</h3>
              <p className="text-sm text-slate-600 mt-1 leading-relaxed">{b.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* TRUST */}
      <section className="bg-slate-950 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <span className="text-xs uppercase tracking-widest font-semibold text-orange-400">Trusted by Local Shopkeepers</span>
            <h2 className="font-display text-3xl sm:text-4xl font-bold tracking-tight mt-3">
              A platform built on trust, safety and community.
            </h2>
            <p className="text-slate-300 mt-4 leading-relaxed">
              We verify every seller, secure every payment, and back you with real human support.
              Your growth is our mission.
            </p>
            <Link to="/sell" className="inline-block mt-6"><Button className="bg-orange-700 hover:bg-orange-800 rounded-full">Join the Marketplace</Button></Link>
          </div>
          <div className="grid grid-cols-2 gap-4">
            {TRUST.map((t) => (
              <div key={t.title} className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 backdrop-blur-xl">
                <t.icon className="w-6 h-6 text-orange-400 mb-3" />
                <h4 className="font-display font-bold">{t.title}</h4>
                <p className="text-sm text-slate-400 mt-1">{t.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="relative bg-gradient-to-br from-orange-700 to-orange-900 rounded-3xl p-10 sm:p-16 overflow-hidden">
          <div className="absolute -right-10 -top-10 w-64 h-64 bg-white/10 rounded-full blur-3xl" />
          <div className="relative">
            <h2 className="font-display text-3xl sm:text-4xl font-bold text-white max-w-xl">Ready to take your shop online?</h2>
            <p className="mt-4 text-orange-100 max-w-lg">Join hundreds of local shopkeepers already selling on FashionConnect.</p>
            <Link to="/sell">
              <Button size="lg" className="mt-8 bg-white text-orange-700 hover:bg-orange-50 rounded-full h-12 px-6">
                Start Selling Free <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
