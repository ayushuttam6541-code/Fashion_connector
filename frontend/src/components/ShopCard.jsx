import { Link } from "react-router-dom";
import { MapPin, Phone, Clock, ShieldCheck, Star, Navigation } from "lucide-react";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { motion } from "framer-motion";

export default function ShopCard({ shop, index = 0 }) {
  const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(shop.address)}`;
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.4, delay: (index % 8) * 0.05 }}
      data-testid={`shop-card-${shop.id}`}
      className="group bg-white border border-slate-200 rounded-xl overflow-hidden hover:-translate-y-1 hover:shadow-lg transition-[transform,box-shadow] duration-300 flex flex-col"
    >
      <div className="relative h-48 overflow-hidden bg-slate-100">
        <img
          src={shop.banner_url || shop.logo_url || "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800"}
          alt={shop.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          loading="lazy"
        />
        {shop.verified && (
          <Badge className="absolute top-3 left-3 bg-emerald-600 text-white gap-1 border-none">
            <ShieldCheck className="w-3 h-3" /> Verified
          </Badge>
        )}
        <div className="absolute top-3 right-3 bg-white/95 rounded-full px-2 py-1 text-xs font-semibold flex items-center gap-1 shadow-sm">
          <Star className="w-3 h-3 fill-amber-500 text-amber-500" /> {shop.rating?.toFixed(1) ?? "4.5"}
        </div>
      </div>
      <div className="p-5 flex-1 flex flex-col">
        <h3 className="font-display font-bold text-lg tracking-tight">{shop.name}</h3>
        <p className="text-xs text-slate-500 mt-1 line-clamp-1">{shop.category || shop.categories?.join(" • ")}</p>

        <div className="mt-3 space-y-1.5 text-sm text-slate-600 flex-1">
          <p className="flex items-start gap-2 line-clamp-2"><MapPin className="w-4 h-4 mt-0.5 shrink-0 text-slate-400" /> {shop.address}</p>
          <p className="flex items-center gap-2"><Phone className="w-4 h-4 text-slate-400" /> {shop.phone}</p>
          <p className="flex items-center gap-2"><Clock className="w-4 h-4 text-slate-400" /> {shop.business_hours}</p>
        </div>

        <div className="flex flex-wrap gap-1 mt-3">
          {(shop.services || []).slice(0, 3).map((s) => (
            <span key={s} className="text-[10px] uppercase tracking-wide bg-slate-100 text-slate-700 rounded-full px-2 py-0.5">{s}</span>
          ))}
        </div>

        <div className="flex gap-2 mt-5">
          <Link to={`/shops/${shop.id}`} className="flex-1" data-testid={`view-shop-${shop.id}`}>
            <Button className="w-full bg-slate-900 hover:bg-slate-800 rounded-full">View Shop</Button>
          </Link>
          <a
            href={mapsUrl}
            target="_blank"
            rel="noopener noreferrer"
            data-testid={`map-shop-${shop.id}`}
            className="inline-flex items-center justify-center w-11 h-10 rounded-full border border-slate-300 hover:border-orange-700 hover:text-orange-700 transition-colors"
            aria-label="Open in Maps"
          >
            <Navigation className="w-4 h-4" />
          </a>
        </div>
      </div>
    </motion.div>
  );
}
