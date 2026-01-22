import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Container from "../components/Container";
import { ordersAPI } from "../api/orders";

type Order = {
  id?: string;
  order_id?: string;
  buyer_id?: string;
  product_id?: string;
  amount?: number;
  total_price?: number;
  status?: string;
};

export default function OrderDetailPage() {
  const { id } = useParams<{ id: string }>();
  const nav = useNavigate();

  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    let mounted = true;

    (async () => {
      try {
        if (!id) {
          if (mounted) {
            setMsg("Missing order id");
            setOrder(null);
            setLoading(false);
          }
          return;
        }

        if (mounted) {
          setLoading(true);
          setMsg("");
          setOrder(null);
        }

        const data = await ordersAPI.getOrder(id);

        if (mounted) setOrder(data);
      } catch (e: any) {
        if (mounted) setMsg(e?.response?.data?.detail ?? "Order not found");
      } finally {
        if (mounted) setLoading(false);
      }
    })();

    return () => {
      mounted = false;
    };
  }, [id]);

  const displayId = order?.id ?? order?.order_id ?? id ?? "";
  const amount = Number(order?.amount ?? order?.total_price ?? 0);

  return (
    <Container>
      <div className="py-8 max-w-3xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold">Order Details</h1>
          <button className="px-4 py-2 border rounded-lg" onClick={() => nav(-1)}>
            Back
          </button>
        </div>

        {loading && <p>Loading...</p>}
        {!loading && msg && <p className="text-red-700 text-sm">{msg}</p>}

        {!loading && order && (
          <div className="bg-white border rounded-xl p-5 space-y-4">
            <div>
              <div className="text-xs text-gray-500">Order ID</div>
              <div className="font-mono break-all">{displayId}</div>
            </div>

            <div>
              <div className="text-xs text-gray-500">Status</div>
              <div className="font-semibold">{order.status ?? "unknown"}</div>
            </div>

            <div>
              <div className="text-xs text-gray-500">Amount</div>
              <div className="font-semibold">${amount.toFixed(2)}</div>
            </div>

            <div>
              <div className="text-xs text-gray-500">Product(s)</div>
              <div className="break-all">{String(order.product_id ?? "—")}</div>
            </div>
          </div>
        )}
      </div>
    </Container>
  );
}
