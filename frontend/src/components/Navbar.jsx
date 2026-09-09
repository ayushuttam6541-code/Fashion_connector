import { Link, useNavigate, useLocation } from "react-router-dom";
import { useState } from "react";
import { ShoppingBag, Menu, X, Search, LogOut, LayoutDashboard, Shield } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { useCart } from "../context/CartContext";
import { Button } from "./ui/button";

export default function Navbar() {
  const { user, logout } = useAuth();
  const { count } = useCart();
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState("");
  const navigate = useNavigate();
  const location = useLocation();

  const submit = (e) => {
    e.preventDefault();
    navigate(`/shops?q=${encodeURIComponent(q)}`);
    setOpen(false);
  };

  const NavLink = ({ to, children, testid }) => (
    <Link
      to={to}
      data-testid={testid}
      className={`px-3 py-2 text-sm font-medium transition-colors hover:text-orange-700 ${
        location.pathname === to ? "text-orange-700" : "text-slate-700"
      }`}
    >{children}</Link>
  );

  return (
    <header className="sticky top-0 z-50 backdrop-blur-xl bg-white/85 border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" data-testid="nav-logo" className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-lg bg-slate-900 text-white flex items-center justify-center font-display font-bold">FC</div>
            <span className="font-display font-bold text-lg tracking-tight">FashionConnect</span>
          </Link>

          <nav className="hidden md:flex items-center gap-1">
            <NavLink to="/" testid="nav-home">Home</NavLink>
            <NavLink to="/shops" testid="nav-shops">Shops</NavLink>
            <NavLink to="/sell" testid="nav-sell">Sell With Us</NavLink>
            <NavLink to="/contact" testid="nav-contact">Contact</NavLink>
          </nav>

          <form onSubmit={submit} className="hidden lg:flex items-center bg-slate-100 rounded-full px-4 py-2 w-72">
            <Search className="w-4 h-4 text-slate-500" />
            <input
              data-testid="nav-search-input"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search shops, ethnic wear..."
              className="bg-transparent outline-none text-sm ml-2 w-full"
            />
          </form>

          <div className="flex items-center gap-2">
            <Link to="/cart" data-testid="nav-cart" className="relative p-2 rounded-full hover:bg-slate-100">
              <ShoppingBag className="w-5 h-5" />
              {count > 0 && (
                <span data-testid="cart-count" className="absolute -top-1 -right-1 bg-orange-700 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">{count}</span>
              )}
            </Link>

            {user ? (
              <div className="hidden md:flex items-center gap-2">
                {user.role === "seller" && (
                  <Link to="/seller/dashboard" data-testid="nav-seller-dashboard">
                    <Button variant="ghost" size="sm"><LayoutDashboard className="w-4 h-4 mr-1" /> Dashboard</Button>
                  </Link>
                )}
                {user.role === "admin" && (
                  <Link to="/admin" data-testid="nav-admin">
                    <Button variant="ghost" size="sm"><Shield className="w-4 h-4 mr-1" /> Admin</Button>
                  </Link>
                )}
                <span className="text-sm text-slate-600">Hi, {user.name?.split(" ")[0]}</span>
                <Button data-testid="nav-logout" variant="outline" size="sm" onClick={logout}><LogOut className="w-4 h-4" /></Button>
              </div>
            ) : (
              <div className="hidden md:flex items-center gap-2">
                <Link to="/login" data-testid="nav-login"><Button variant="ghost" size="sm">Login</Button></Link>
                <Link to="/sell" data-testid="nav-cta-sell">
                  <Button size="sm" className="bg-orange-700 hover:bg-orange-800 rounded-full">Become a Seller</Button>
                </Link>
              </div>
            )}

            <button data-testid="nav-menu-toggle" className="md:hidden p-2" onClick={() => setOpen(!open)}>
              {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {open && (
          <div className="md:hidden py-4 border-t border-slate-200 space-y-2">
            <form onSubmit={submit} className="flex items-center bg-slate-100 rounded-full px-4 py-2">
              <Search className="w-4 h-4 text-slate-500" />
              <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search..." className="bg-transparent outline-none text-sm ml-2 w-full" />
            </form>
            <NavLink to="/" testid="mnav-home">Home</NavLink>
            <NavLink to="/shops" testid="mnav-shops">Shops</NavLink>
            <NavLink to="/sell" testid="mnav-sell">Sell With Us</NavLink>
            <NavLink to="/contact" testid="mnav-contact">Contact</NavLink>
            {user ? (
              <>
                {user.role === "seller" && <NavLink to="/seller/dashboard" testid="mnav-dash">Dashboard</NavLink>}
                {user.role === "admin" && <NavLink to="/admin" testid="mnav-admin">Admin</NavLink>}
                <button data-testid="mnav-logout" onClick={logout} className="w-full text-left px-3 py-2 text-sm text-red-600">Logout</button>
              </>
            ) : (
              <>
                <NavLink to="/login" testid="mnav-login">Login</NavLink>
                <NavLink to="/register" testid="mnav-register">Register</NavLink>
              </>
            )}
          </div>
        )}
      </div>
    </header>
  );
}
