import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Container from "../components/Container";
import type { Product } from "../types/models";
import { deleteProduct, listMyProducts } from "../api/products";
import { getSession } from "../auth/session";

const toImgUrl = (raw?: string) => {
  if (!raw) return "/no-image.png";
  if (raw.startsWith("http")) return raw;
  return `http://localhost:8000${raw}`;
};

export default function MyProducts() {
  const navigate = useNavigate();
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Container>
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div>
          <h1 className="text-2xl font-semibold">My Products</h1>
          <p className="text-gray-600 text-sm">Seller ID: {seller_id}</p>
        </div>
        <button className="border rounded-lg px-3 py-2 text-sm" onClick={load}>
          Refresh
        </button>
      </div>

      {loading && <p className="mt-4">Loading...</p>}
      {err && <p className="mt-4 text-red-700 text-sm">{err}</p>}

      {!loading && !err && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
          {items.map((p) => {
            // ✅ Prioridad: images[0] (como tu ProductCard) -> image_url (fallback)
            const rawImg = (p as any)?.images?.[0] || (p as any)?.image_url || "";
            const src = toImgUrl(rawImg);

            return (
              <div
                key={p.id}
                className="border rounded-xl overflow-hidden bg-white hover:shadow-lg transition-shadow"
              >
                {/* Product Image */}
                <img
                  src={src}
                  alt={p.title}
                  className="w-full h-48 object-cover bg-gray-100"
                  onError={(e) => {
                    (e.currentTarget as HTMLImageElement).src = "/no-image.png";
                  }}
                />

                {/* Product Details */}
                <div className="p-4">
                  <div className="font-semibold text-lg truncate">{p.title}</div>

                  <div className="text-sm text-gray-600 line-clamp-2 mt-1">
                    {p.description}
                  </div>

                  <div className="text-xs text-gray-500 mt-2">{p.category}</div>

                  <div className="font-bold text-lg mt-2 text-blue-600">
                    ${p.price.toFixed(2)}
                  </div>

                  {/* ✅ BOTONES: Edit + Delete */}
                  <div className="mt-3 grid grid-cols-2 gap-2">
                    <button
                      className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-3 py-2 text-sm transition-colors"
                      onClick={() => navigate(`/my-products/${p.id}/edit`)}
                    >
                      Editar
                    </button>

                    <button
                      className="w-full bg-red-500 hover:bg-red-600 text-white rounded-lg px-3 py-2 text-sm transition-colors"
                      onClick={() => onDelete(p.id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            );
          })}

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
