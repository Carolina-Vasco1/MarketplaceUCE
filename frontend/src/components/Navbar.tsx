import { Link, useNavigate } from "react-router-dom";
import { clearToken, getToken } from "../auth/token";
import { getSession } from "../auth/session";

export default function Navbar() {
  const nav = useNavigate();
  const token = getToken();
  const session = getSession();

  return (
    <div className="sticky top-0 bg-white border-b z-50">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="font-bold text-lg">Marketplace UCE</Link>

        <div className="flex items-center gap-3 text-sm">
          <Link to="/" className="hover:underline">Home</Link>

          {!token && (
            <>
              <Link to="/login" className="hover:underline">Login</Link>
              <Link to="/register" className="hover:underline">OTP Register</Link>
            </>
          )}

          {token && (session?.role === "seller" || session?.role === "admin") && (
            <>
              <Link to="/sell" className="hover:underline">Sell</Link>
              <Link to="/my-products" className="hover:underline">My Products</Link>
            </>
          )}

          {token && session?.role === "admin" && (
            <Link to="/admin" className="hover:underline">Admin</Link>
          )}

          {token && (
            <button
              className="bg-black text-white px-3 py-1 rounded-lg"
              onClick={() => {
                clearToken();
                nav("/");
              }}
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
