import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Container from "../components/Container";
import type { Product } from "../types/models";
import { getProduct } from "../api/products";
import { createOrderAndPay } from "../api/orders";
import { getToken } from "../auth/token";

function getEmailFromJwt(token: string): string | null {
  try {
    const payload = token.split(".")[1];
    const json = JSON.parse(atob(payload));
    return json?.sub ?? json?.email ?? null;
  } catch {
    return null;
  }
}

export default function ProductDetail() {
  const { id } = useParams();
  const [p, setP] = useState<Product | null>(null);
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(true);
  const [buying, setBuying] = useState(false);

  async function load() {
    setErr("");
    setLoading(true);
    try {
      if (!id) throw new Error("Invalid ID");
      const data = await getProduct(id);
      setP(data);
    } catch (e: any) {
      console.error("[ProductDetail] load error:", e);
      setErr(e?.response?.data?.detail ?? "Unable to load the product.");
    } finally {
      setLoading(false);
    }
  }

  async function onBuy() {
    setErr("");

    const token = getToken();
    if (!token) {
      alert("Debes iniciar sesión para comprar.");
      return;
    }

    const buyerEmail = getEmailFromJwt(token);
    if (!buyerEmail) {
      alert("Token inválido. Vuelve a iniciar sesión.");
      return;
    }

    if (!p?.id) {
      alert("Producto inválido.");
      return;
    }

    setBuying(true);
    try {
      const res = await createOrderAndPay({
        product_id: p.id,
        amount: Number(p.price),
      });

      if (res?.approval_url) {
        window.location.href = res.approval_url;
        return;
      }

      alert(`Orden creada: ${res.order_id}`);
    } catch (e: any) {
      console.error("[BUY] error:", e);
      const msg =
        e?.response?.data?.detail ?? e?.message ?? "Buy failed (check backend).";
      setErr(msg);
      alert(msg);
    } finally {
      setBuying(false);
    }
  }

  useEffect(() => {
    load();
  }, [id]);

  return (
    <Container>
      {loading && <p>Loading...</p>}
      {err && <p className="text-red-700 text-sm">{err}</p>}

      {p && (
        <div className="border rounded-xl p-4 bg-white">
          <h1 className="text-2xl font-semibold">{p.title}</h1>
          <p className="text-gray-600 mt-2">{p.description}</p>
          <p className="font-bold mt-3">${Number(p.price).toFixed(2)}</p>

          <div className="mt-4 text-sm text-gray-500">
            <div>Seller: {p.seller_id}</div>
            <div>Category: {p.category_id || "-"}</div>
          </div>

          <button
            className="mt-4 bg-black text-white rounded-lg px-4 py-2 text-sm disabled:opacity-60"
            onClick={onBuy}
            disabled={buying}
          >
            {buying ? "Processing..." : "Buy"}
          </button>
        </div>
      )}
    </Container>
  );
}
