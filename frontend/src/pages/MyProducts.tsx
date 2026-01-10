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
            <div key={p.id} className="border rounded-xl p-4 bg-white">
              <div className="font-semibold">{p.title}</div>
              <div className="text-sm text-gray-600 line-clamp-2">
                {p.description}
              </div>
              <div className="font-bold mt-2">
                ${p.price.toFixed(2)}
              </div>
              <button
                className="mt-3 w-full border rounded-lg px-3 py-2 text-sm"
                onClick={() => onDelete(p.id)}
              >
                Delete
              </button>
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
