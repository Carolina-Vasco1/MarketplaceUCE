import { useEffect, useState } from "react";
import Container from "../components/Container";
import type { Product } from "../types/models";
import { deleteProduct, listMyProducts } from "../api/products";
import { getSession } from "../auth/session";

export default function MyProducts() {
  const session = getSession();
  const seller_id = session?.user_id || "";

  const [items, setItems] = useState<Product[]>([]);
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(true);

  async function load() {
    setErr("");
    setLoading(true);
    try {
      const data = await listMyProducts(seller_id);
      setItems(data);
    } catch (e: any) {
      setErr(e?.response?.data?.detail ?? "Unable to load your products.");
    } finally {
      setLoading(false);
    }
  }

  async function onDelete(id: string) {
    if (!confirm("Delete product?")) return;
    try {
      await deleteProduct(id);
      await load();
    } catch (e: any) {
      alert(e?.response?.data?.detail ?? "Unable to delete.");
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <Container>
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div>
          <h1 className="text-2xl font-semibold">My Products</h1>
          <p className="text-gray-600 text-sm">Seller ID: {seller_id}</p>
        </div>
        <button
          className="border rounded-lg px-3 py-2 text-sm"
          onClick={load}
        >
          Refresh
        </button>
      </div>

      {loading && <p className="mt-4">Loading...</p>}
      {err && <p className="mt-4 text-red-700 text-sm">{err}</p>}

      {!loading && !err && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
          {items.map((p) => (
            <div key={p.id} className="border rounded-xl overflow-hidden bg-white hover:shadow-lg transition-shadow">
              {/* Product Image */}
              {p.image_url && (
                <img
                  src={p.image_url}
                  alt={p.title}
                  className="w-full h-48 object-cover"
                />
              )}
              {!p.image_url && (
                <div className="w-full h-48 bg-gray-200 flex items-center justify-center text-gray-400">
                  No image
                </div>
              )}
              
              {/* Product Details */}
              <div className="p-4">
                <div className="font-semibold text-lg truncate">{p.title}</div>
                <div className="text-sm text-gray-600 line-clamp-2 mt-1">
                  {p.description}
                </div>
                <div className="text-xs text-gray-500 mt-2">
                  {p.category}
                </div>
                <div className="font-bold text-lg mt-2 text-blue-600">
                  ${p.price.toFixed(2)}
                </div>
                <button
                  className="mt-3 w-full bg-red-500 hover:bg-red-600 text-white rounded-lg px-3 py-2 text-sm transition-colors"
                  onClick={() => onDelete(p.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
          {items.length === 0 && (
            <div className="border rounded-xl p-4 text-gray-600">
              You have no published products.
            </div>
          )}
        </div>
      )}
    </Container>
  );
}
