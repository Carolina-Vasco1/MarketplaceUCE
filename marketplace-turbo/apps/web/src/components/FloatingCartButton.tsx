import { Link } from "react-router-dom";
import { useCart } from "../store/cartStore";
import { getToken } from "../auth/token";

export default function FloatingCartButton() {
  const token = getToken();
  const { items } = useCart();

  // ✅ si no hay login, no se muestra
  if (!token) return null;

  const count = items.reduce((acc, i) => acc + i.quantity, 0);

  // ✅ si quieres que NO salga cuando está vacío, descomenta esto:
  // if (count === 0) return null;

  return (
    <Link
      to="/cart"
      className="
        fixed bottom-5 right-5 z-50
        md:hidden
        flex items-center gap-2
        rounded-full bg-primary-600 text-white
        px-4 py-3 shadow-lg
        hover:bg-primary-700 active:scale-95
        transition
      "
      aria-label="Open cart"
    >
      <span className="text-lg">🛒</span>
      <span className="font-semibold">Cart</span>

      <span
        className="
          ml-1
          min-w-6 h-6
          px-2
          rounded-full bg-white text-primary-700
          text-xs font-bold
          flex items-center justify-center
        "
      >
        {count}
      </span>
    </Link>
  );
}
