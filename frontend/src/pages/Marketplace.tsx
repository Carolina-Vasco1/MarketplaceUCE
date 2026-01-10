import { useEffect, useState } from "react";
import Container from "../components/Container";
import ProductCard from "../components/ProductCard";
import type { Product } from "../types/models";
import { listProducts } from "../api/products";

export default function Marketplace() {
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<Product[]>([]);
  const [err, setErr] = useState("");

  async function load() {
    setErr("");
    setLoading(true);
    try {
      const data = await listProducts();
      setItems(data);
    } catch (e: any) {
      setErr(
        e?.response?.data?.detail ??
          "Unable to load products (check gateway/backend)."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <Container>
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div>
          <h1 className="text-2xl font-semibold">Products</h1>
          <p className="text-gray-600">
            Responsive marketplace (desktop + mobile)
          </p>
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
            <ProductCard key={p.id} p={p} />
          ))}
          {items.length === 0 && (
            <div className="border rounded-xl p-4 text-gray-600">
              No products yet. If you are a seller, publish one.
            </div>
          )}
        </div>
      )}
    </Container>
  );
}
