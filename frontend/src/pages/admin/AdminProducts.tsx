import { useEffect, useState } from "react";
import Container from "../../components/Container";
import AdminSidebar from "../../components/AdminSidebar";
import type { Product } from "../../types/models";
import {
  adminDeleteProduct,
  adminListProducts,
} from "../../api/admin";

export default function AdminProducts() {
  const [items, setItems] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

  async function load() {
    setErr("");
    setLoading(true);
    try {
      setItems(await adminListProducts());
    } catch (e: any) {
      setErr(
        e?.response?.data?.detail ??
          "Unable to load admin products (missing endpoint)."
      );
    } finally {
      setLoading(false);
    }
  }

  async function onDelete(id: string) {
    if (!confirm("Delete product?")) return;
    try {
      await adminDeleteProduct(id);
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
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="md:col-span-1">
          <AdminSidebar />
        </div>

        <div className="md:col-span-3">
          <h1 className="text-2xl font-semibold mb-3">Products (Admin)</h1>

          {loading && <p>Loading...</p>}
          {err && <p className="text-red-700 text-sm">{err}</p>}

          {!loading && !err && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {items.map((p) => (
                <div key={p.id} className="border rounded-xl p-4 bg-white">
                  <div className="font-semibold">{p.title}</div>
                  <div className="text-sm text-gray-600 line-clamp-2">
                    {p.description}
                  </div>
                  <div className="font-bold mt-2">
                    ${p.price.toFixed(2)}
                  </div>
                  <div className="text-xs text-gray-500 mt-2">
                    seller: {p.seller_id}
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
                <div className="text-gray-600">No products found.</div>
              )}
            </div>
          )}
        </div>
      </div>
    </Container>
  );
}
