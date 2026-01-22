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

  const [adminOpen, setAdminOpen] = useState(false);
  const [userOpen, setUserOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isActive = (path: string) =>
    location.pathname === path || location.pathname.startsWith(path + "/");

  const navLinkClass = (path: string) =>
    `px-3 py-2 rounded-lg transition-colors text-sm font-medium ${
      isActive(path) ? "bg-primary-500 text-white" : "text-gray-700 hover:bg-gray-100"
    }`;

  const closeAll = () => {
    setAdminOpen(false);
    setUserOpen(false);
    setMobileMenuOpen(false);
  };

  const onLogout = () => {
    clearToken();
    window.dispatchEvent(new CustomEvent("logout"));
    closeAll();
    nav("/");
  };

  const showOrdersLinks = !!token; // ✅ cualquier usuario logueado (buyer/seller/admin)
  const showSellerLinks = !!token && (session?.role === "seller" || session?.role === "admin");
  const showAdminLinks = !!token && session?.role === "admin";

  return (
    <nav className="sticky top-0 bg-white border-b border-gray-200 shadow-sm z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16 gap-3">
          {/* Logo */}
          <Link
            to="/"
            onClick={closeAll}
            className="flex items-center gap-2 font-bold text-xl text-primary-600 hover:text-primary-700 transition-colors min-w-0"
          >
            <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-600 rounded-lg flex items-center justify-center text-white text-sm font-bold">
              M
            </div>
            <span className="hidden sm:inline truncate">Marketplace</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-1">
            <Link to="/" className={navLinkClass("/")} onClick={closeAll}>
              Home
            </Link>
            <Link to="/search" className={navLinkClass("/search")} onClick={closeAll}>
              Search
            </Link>
            <Link
              to="/recommendations"
              className={navLinkClass("/recommendations")}
              onClick={closeAll}
            >
              Recommendations
            </Link>

            {/* Cart visible en desktop */}
            <Link to="/cart" className={navLinkClass("/cart")} onClick={closeAll}>
              Cart {cartItems.length > 0 ? `(${cartItems.length})` : ""}
            </Link>

            {/* ✅ Orders al lado de Cart (buyer/seller/admin) */}
            {showOrdersLinks && (
              <Link to="/my-orders" className={navLinkClass("/my-orders")} onClick={closeAll}>
                Orders
              </Link>
            )}

            {!token && (
              <>
                <Link to="/login" className={navLinkClass("/login")} onClick={closeAll}>
                  Login
                </Link>
                <Link to="/register" className={navLinkClass("/register")} onClick={closeAll}>
                  Register
                </Link>
              </>
            )}

            {showSellerLinks && (
              <>
                <Link to="/sell" className={navLinkClass("/sell")} onClick={closeAll}>
                  Sell
                </Link>
                <Link to="/my-products" className={navLinkClass("/my-products")} onClick={closeAll}>
                  My Products
                </Link>
                <Link to="/analytics" className={navLinkClass("/analytics")} onClick={closeAll}>
                  Analytics
                </Link>
              </>
            )}

            {/* Admin dropdown */}
            {showAdminLinks && (
              <div className="relative">
                <button
                  onClick={() => {
                    setAdminOpen((v) => !v);
                    setUserOpen(false);
                  }}
                  className="px-3 py-2 rounded-lg bg-secondary-500 text-white hover:bg-secondary-600 transition-colors font-semibold flex items-center gap-2 text-sm"
                >
                  Admin <span className="text-xs">▼</span>
                </button>

                {adminOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg py-2">
                    <Link
                      to="/admin"
                      onClick={closeAll}
                      className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                    >
                      Dashboard
                    </Link>
                    <Link
                      to="/admin/users"
                      onClick={closeAll}
                      className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                    >
                      Users
                    </Link>
                    <Link
                      to="/admin/products"
                      onClick={closeAll}
                      className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                    >
                      Products
                    </Link>
                    <Link
                      to="/admin/reports"
                      onClick={closeAll}
                      className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                    >
                      Reports
                    </Link>
                  </div>
                )}
              </div>
            )}

            {/* User dropdown */}
            {token && (
              <div className="relative ml-3 pl-3 border-l border-gray-200">
                <button
                  onClick={() => {
                    setUserOpen((v) => !v);
                    setAdminOpen(false);
                  }}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors text-sm"
                >
                  👤 {session?.role || "User"} <span className="text-xs">▼</span>
                </button>

                {userOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg py-2">
                    <Link
                      to="/profile"
                      onClick={closeAll}
                      className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                    >
                      Profile
                    </Link>
                    <Link
                      to="/reviews"
                      onClick={closeAll}
                      className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                    >
                      My Reviews
                    </Link>
                    <button
                      onClick={onLogout}
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
            onClick={() => {
              setMobileMenuOpen((v) => !v);
              setAdminOpen(false);
              setUserOpen(false);
            }}
            className="md:hidden p-2 hover:bg-gray-100 rounded-lg"
            aria-label="Open menu"
          >
            ☰
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden pb-4 space-y-2 border-t border-gray-200 pt-4">
            <Link to="/" onClick={closeAll} className="block px-3 py-2 rounded-lg hover:bg-gray-100">
              Home
            </Link>
            <Link
              to="/search"
              onClick={closeAll}
              className="block px-3 py-2 rounded-lg hover:bg-gray-100"
            >
              Search
            </Link>
            <Link
              to="/recommendations"
              onClick={closeAll}
              className="block px-3 py-2 rounded-lg hover:bg-gray-100"
            >
              Recommendations
            </Link>

            {/* ✅ Cart en móvil */}
            <Link to="/cart" onClick={closeAll} className="block px-3 py-2 rounded-lg hover:bg-gray-100">
              Cart {cartItems.length > 0 ? `(${cartItems.length})` : ""}
            </Link>

            {/* ✅ Orders al lado de Cart (en móvil también) */}
            {showOrdersLinks && (
              <Link
                to="/my-orders"
                onClick={closeAll}
                className="block px-3 py-2 rounded-lg hover:bg-gray-100"
              >
                Orders
              </Link>
            )}

            {!token && (
              <>
                <Link
                  to="/login"
                  onClick={closeAll}
                  className="block px-3 py-2 rounded-lg hover:bg-gray-100"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  onClick={closeAll}
                  className="block px-3 py-2 rounded-lg hover:bg-gray-100"
                >
                  Register
                </Link>
              </>
            )}

            {showSellerLinks && (
              <>
                <Link to="/sell" onClick={closeAll} className="block px-3 py-2 rounded-lg hover:bg-gray-100">
                  Sell
                </Link>
                <Link
                  to="/my-products"
                  onClick={closeAll}
                  className="block px-3 py-2 rounded-lg hover:bg-gray-100"
                >
                  My Products
                </Link>
                <Link
                  to="/analytics"
                  onClick={closeAll}
                  className="block px-3 py-2 rounded-lg hover:bg-gray-100"
                >
                  Analytics
                </Link>
              </>
            )}

            {showAdminLinks && (
              <>
                <Link
                  to="/admin"
                  onClick={closeAll}
                  className="block px-3 py-2 rounded-lg hover:bg-gray-100"
                >
                  Admin Dashboard
                </Link>
                <Link
                  to="/admin/users"
                  onClick={closeAll}
                  className="block px-3 py-2 rounded-lg hover:bg-gray-100"
                >
                  Admin Users
                </Link>
                <Link
                  to="/admin/products"
                  onClick={closeAll}
                  className="block px-3 py-2 rounded-lg hover:bg-gray-100"
                >
                  Admin Products
                </Link>
                <Link
                  to="/admin/reports"
                  onClick={closeAll}
                  className="block px-3 py-2 rounded-lg hover:bg-gray-100"
                >
                  Admin Reports
                </Link>
              </>
            )}

            {token && (
              <>
                <Link
                  to="/profile"
                  onClick={closeAll}
                  className="block px-3 py-2 rounded-lg hover:bg-gray-100"
                >
                  Profile
                </Link>
                <Link
                  to="/reviews"
                  onClick={closeAll}
                  className="block px-3 py-2 rounded-lg hover:bg-gray-100"
                >
                  My Reviews
                </Link>
                <button
                  onClick={onLogout}
                  className="w-full text-left px-3 py-2 text-red-600 rounded-lg hover:bg-red-50 border-t"
                >
                  Logout
                </button>
              </>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}
