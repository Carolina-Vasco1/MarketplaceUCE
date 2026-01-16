import { Link, useNavigate, useLocation } from "react-router-dom";
import { clearToken, getToken } from "../auth/token";
import { getSession } from "../auth/session";
import { useState } from "react";
import { useCart } from "../store/cartStore";

export default function Navbar() {
  const nav = useNavigate();
  const location = useLocation();
  const token = getToken();
  const session = getSession();
  const { items: cartItems } = useCart();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isActive = (path: string) => location.pathname.startsWith(path);

  const navLinkClass = (path: string) =>
    `px-3 py-2 rounded-lg transition-colors ${
      isActive(path)
        ? "bg-primary-500 text-white font-semibold"
        : "text-gray-700 hover:bg-gray-100"
    }`;

  return (
    <nav className="sticky top-0 bg-white border-b border-gray-200 shadow-sm z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link
            to="/"
            className="flex items-center gap-2 font-bold text-xl text-primary-600 hover:text-primary-700 transition-colors"
          >
            <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-600 rounded-lg flex items-center justify-center text-white text-sm font-bold">
              M
            </div>
            <span className="hidden sm:inline">Marketplace</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-1">
            <Link to="/" className={navLinkClass("/")}>
              🏠 Home
            </Link>
            <Link to="/search" className={navLinkClass("/search")}>
              🔍 Search
            </Link>
            <Link to="/recommendations" className={navLinkClass("/recommendations")}>
              ⭐ Recommendations
            </Link>
            <Link to="/cart" className={navLinkClass("/cart")}>
              🛒 Cart {cartItems.length > 0 && `(${cartItems.length})`}
            </Link>

            {!token && (
              <>
                <Link to="/login" className={navLinkClass("/login")}>
                  Login
                </Link>
                <Link to="/register" className={navLinkClass("/register")}>
                  Register
                </Link>
              </>
            )}

            {token && (session?.role === "seller" || session?.role === "admin") && (
              <>
                <Link to="/sell" className={navLinkClass("/sell")}>
                  📦 Sell
                </Link>
                <Link to="/my-products" className={navLinkClass("/my-products")}>
                  My Products
                </Link>
                <Link to="/my-orders" className={navLinkClass("/my-orders")}>
                  📋 Orders
                </Link>
                <Link to="/analytics" className={navLinkClass("/analytics")}>
                  📊 Analytics
                </Link>
              </>
            )}

            {token && session?.role === "admin" && (
              <div className="relative">
                <button
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  className="px-3 py-2 rounded-lg bg-secondary-500 text-white hover:bg-secondary-600 transition-colors font-semibold flex items-center gap-2"
                >
                  ⚙️ Admin
                  <span className="text-xs">▼</span>
                </button>
                {dropdownOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg py-2">
                    <Link
                      to="/admin"
                      className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                    >
                      Dashboard
                    </Link>
                    <Link
                      to="/admin/users"
                      className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                    >
                      Users
                    </Link>
                    <Link
                      to="/admin/products"
                      className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                    >
                      Products
                    </Link>
                    <Link
                      to="/admin/reports"
                      className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                    >
                      Reports
                    </Link>
                  </div>
                )}
              </div>
            )}

            {token && (
              <div className="relative ml-4 pl-4 border-l border-gray-300">
                <button
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  👤 {session?.role || "User"}
                  <span className="text-xs">▼</span>
                </button>
                {dropdownOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg py-2">
                    <Link
                      to="/profile"
                      className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                    >
                      Profile
                    </Link>
                    <Link
                      to="/reviews"
                      className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                    >
                      My Reviews
                    </Link>
                    <button
                      onClick={() => {
                        clearToken();
                        // Dispatch logout event for cart clearing
                        window.dispatchEvent(new CustomEvent("logout"));
                        setDropdownOpen(false);
                        nav("/");
                      }}
                      className="w-full text-left px-4 py-2 text-red-600 hover:bg-red-50 border-t"
                    >
                      Logout
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 hover:bg-gray-100 rounded-lg"
          >
            ☰
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden pb-4 space-y-2 border-t border-gray-200 pt-4">
            <Link to="/" className="block px-3 py-2 rounded-lg hover:bg-gray-100">
              Home
            </Link>
            <Link to="/search" className="block px-3 py-2 rounded-lg hover:bg-gray-100">
              Search
            </Link>
            <Link to="/recommendations" className="block px-3 py-2 rounded-lg hover:bg-gray-100">
              Recommendations
            </Link>

            {!token && (
              <>
                <Link to="/login" className="block px-3 py-2 rounded-lg hover:bg-gray-100">
                  Login
                </Link>
                <Link to="/register" className="block px-3 py-2 rounded-lg hover:bg-gray-100">
                  Register
                </Link>
              </>
            )}

            {token && (
              <button
                onClick={() => {
                  clearToken();
                  setMobileMenuOpen(false);
                  nav("/");
                }}
                className="w-full text-left px-3 py-2 text-red-600 rounded-lg hover:bg-red-50"
              >
                Logout
              </button>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}
