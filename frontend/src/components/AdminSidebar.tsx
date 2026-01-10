import { Link } from "react-router-dom";
import type { Product } from "../types/models";

export default function ProductCard({ p }: { p: Product }) {
  return (
    <div className="border rounded-xl p-4 flex flex-col gap-2 bg-white shadow-sm">
      <div className="font-semibold text-lg line-clamp-1">{p.title}</div>
      <div className="text-sm text-gray-600 line-clamp-2">{p.description}</div>
      <div className="font-bold">${p.price.toFixed(2)}</div>
      <Link
        to={`/products/${p.id}`}
        className="mt-2 inline-flex justify-center bg-black text-white rounded-lg px-3 py-2 text-sm"
      >
        Ver detalle
      </Link>
    </div>
  );
}
