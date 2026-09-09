import { Link } from "react-router-dom";
import { Instagram, Facebook, Twitter, Mail, MapPin, Phone } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-slate-950 text-slate-300 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 grid md:grid-cols-4 gap-10">
        <div>
          <div className="flex items-center gap-2 mb-4">
            <div className="w-9 h-9 rounded-lg bg-orange-700 text-white flex items-center justify-center font-display font-bold">FC</div>
            <span className="font-display font-bold text-lg text-white">FashionConnect</span>
          </div>
          <p className="text-sm text-slate-400 leading-relaxed">
            Bihar's fastest-growing B2B fashion marketplace. Empowering local shopkeepers with digital storefronts.
          </p>
          <div className="flex gap-3 mt-4">
            <button data-testid="footer-instagram" className="p-2 rounded-full bg-slate-800 hover:bg-orange-700 transition-colors" aria-label="Instagram"><Instagram className="w-4 h-4" /></button>
            <button data-testid="footer-facebook" className="p-2 rounded-full bg-slate-800 hover:bg-orange-700 transition-colors" aria-label="Facebook"><Facebook className="w-4 h-4" /></button>
            <button data-testid="footer-twitter" className="p-2 rounded-full bg-slate-800 hover:bg-orange-700 transition-colors" aria-label="Twitter"><Twitter className="w-4 h-4" /></button>
          </div>
        </div>
        <div>
          <h4 className="font-display font-semibold text-white mb-4">For Shoppers</h4>
          <ul className="space-y-2 text-sm">
            <li><Link to="/shops" className="hover:text-orange-500">Browse Shops</Link></li>
            <li><Link to="/shops?category=Men" className="hover:text-orange-500">Men's Fashion</Link></li>
            <li><Link to="/shops?category=Women" className="hover:text-orange-500">Women's Fashion</Link></li>
            <li><Link to="/shops?category=Kids" className="hover:text-orange-500">Kids Wear</Link></li>
            <li><Link to="/shops?category=Ethnic Wear" className="hover:text-orange-500">Ethnic Wear</Link></li>
          </ul>
        </div>
        <div>
          <h4 className="font-display font-semibold text-white mb-4">For Sellers</h4>
          <ul className="space-y-2 text-sm">
            <li><Link to="/sell" className="hover:text-orange-500">Register Your Shop</Link></li>
            <li><Link to="/sell" className="hover:text-orange-500">Start Selling Free</Link></li>
            <li><Link to="/seller/dashboard" className="hover:text-orange-500">Seller Dashboard</Link></li>
            <li><Link to="/contact" className="hover:text-orange-500">Seller Support</Link></li>
          </ul>
        </div>
        <div>
          <h4 className="font-display font-semibold text-white mb-4">Contact</h4>
          <ul className="space-y-2 text-sm">
            <li className="flex items-start gap-2"><MapPin className="w-4 h-4 mt-0.5" /> Patna, Bihar 800001</li>
            <li className="flex items-center gap-2"><Phone className="w-4 h-4" /> +91 854 084 6184</li>
            <li className="flex items-center gap-2"><Mail className="w-4 h-4" /> hello@fashionconnect.in</li>
          </ul>
        </div>
      </div>
      <div className="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
        © {new Date().getFullYear()} FashionConnect. Made with love for local shopkeepers of Patna.
      </div>
    </footer>
  );
}
