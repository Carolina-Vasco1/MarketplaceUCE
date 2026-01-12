import { Link } from "react-router-dom";
import type { Product } from "../types/models";

export default function ProductCard({ p }: { p: Product }) {
  const img = p.images?.[0];

  return (
    <div className="border rounded-xl p-4 flex flex-col gap-2 bg-white shadow-sm">
      {img && (
        <img
          src={`http://localhost:8000${img}`}
          className="w-full h-40 object-cover rounded-lg"
          alt={p.title}
        />
      )}

      <div className="font-semibold text-lg line-clamp-1">{p.title}</div>
      <div className="text-sm text-gray-600 line-clamp-2">{p.description}</div>
      <div className="font-bold">${p.price.toFixed(2)}</div>

      <Link
        to={`/products/${p.id}`}
        className="mt-2 inline-flex justify-center bg-black text-white rounded-lg px-3 py-2 text-sm"
      >
        View details
      </Link>
    </div>
  );
}
