import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Container from "../components/Container";
import type { Product } from "../types/models";
import { getProduct } from "../api/products";

export default function ProductDetail() {
  const { id } = useParams();
  const [p, setP] = useState<Product | null>(null);
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      setErr("");
      setLoading(true);
      try {
        if (!id) throw new Error("Invalid ID");
        const data = await getProduct(id);
        setP(data);
      } catch (e: any) {
        setErr(e?.response?.data?.detail ?? "Unable to load the product.");
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  return (
    <Container>
      {loading && <p>Loading...</p>}
      {err && <p className="text-red-700 text-sm">{err}</p>}
      {p && (
        <div className="border rounded-xl p-4 bg-white">
          <h1 className="text-2xl font-semibold">{p.title}</h1>
          <p className="text-gray-600 mt-2">{p.description}</p>
          <p className="font-bold mt-3">${p.price.toFixed(2)}</p>

          <div className="mt-4 text-sm text-gray-500">
            <div>Seller: {p.seller_id}</div>
            <div>Category: {p.category_id || "-"}</div>
          </div>

          <button className="mt-4 bg-black text-white rounded-lg px-4 py-2 text-sm">
            Buy (integrates with Order/PayPal)
          </button>
        </div>
      )}
    </Container>
  );
}
