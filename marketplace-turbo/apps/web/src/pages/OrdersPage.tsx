import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Container from "../components/Container";
import { ordersAPI } from "../api/orders";

type OrderRow = {
  id?: string;
  order_id?: string;
  buyer_id?: string;
  product_id?: string;
  amount?: number;
  total_price?: number;
  status?: string;
  created_at?: string | null;
};

export default function OrdersPage() {
  const nav = useNavigate();
  const [orders, setOrders] = useState<OrderRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    loadOrders();
  }, []);

  const normalize = (o: any): OrderRow => {
    const id = o?.id ?? o?.order_id;
    const amount =
      typeof o?.amount === "number"
        ? o.amount
        : typeof o?.total_price === "number"
        ? o.total_price
        : 0;

    return { ...o, id, amount, created_at: o?.created_at ?? null };
  };

  const loadOrders = async () => {
    try {
      setLoading(true);
      const data = await ordersAPI.getMyOrders();
      const raw = Array.isArray(data) ? data : Array.isArray(data?.orders) ? data.orders : [];
      setOrders(raw.map(normalize));
    } catch {
      setOrders([]);
    } finally {
      setLoading(false);
    }
  };

  const statusBadge = (status: string) => {
    switch ((status || "").toLowerCase()) {
      case "created":
      case "pending":
        return "bg-yellow-100 text-yellow-700";
      case "confirmed":
        return "bg-blue-100 text-blue-700";
      case "shipped":
        return "bg-purple-100 text-purple-700";
      case "delivered":
      case "completed":
        return "bg-green-100 text-green-700";
      case "cancelled":
        return "bg-red-100 text-red-700";
      default:
        return "bg-gray-100 text-gray-700";
    }
  };

  const filteredOrders =
    filter === "all"
      ? orders
      : orders.filter((o) => (o.status || "").toLowerCase() === filter);

  if (loading) {
    return (
      <Container>
        <div className="py-12 text-center">
          <div className="inline-block animate-spin text-4xl">⏳</div>
        </div>
      </Container>
    );
  }

  return (
    <Container>
      <div className="py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">My Orders</h1>

        <div className="flex gap-2 mb-6 flex-wrap">
          {["all", "created", "confirmed", "shipped", "delivered", "cancelled"].map(
            (s) => (
              <button
                key={s}
                onClick={() => setFilter(s)}
                className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                  filter === s
                    ? "bg-black text-white"
                    : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                }`}
              >
                {s === "created" ? "Pending" : s.charAt(0).toUpperCase() + s.slice(1)}
              </button>
            )
          )}
        </div>

        {filteredOrders.length > 0 ? (
          <div className="space-y-4">
            {filteredOrders.map((order) => {
              const id = order.id ?? order.order_id ?? "";
              const shortId = id ? id.slice(0, 8) : "N/A";
              const total = Number(order.amount ?? 0);

              const dateText =
                order.created_at && !Number.isNaN(Date.parse(order.created_at))
                  ? new Date(order.created_at).toLocaleDateString()
                  : "—";

              return (
                <div
                  key={id || `${shortId}-${Math.random()}`}
                  className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
                >
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <p className="font-semibold text-gray-900">Order #{shortId}</p>
                      <p className="text-sm text-gray-600">{dateText}</p>
                    </div>

                    <span
                      className={`px-3 py-1 rounded-full text-sm font-semibold ${statusBadge(
                        order.status || ""
                      )}`}
                    >
                      {(order.status || "").toLowerCase() === "created"
                        ? "pending"
                        : order.status || "unknown"}
                    </span>
                  </div>

                  <div className="mb-4 pb-4 border-b">
                    <p className="text-sm text-gray-600 mb-2 font-semibold">Items</p>
                    <div className="text-sm text-gray-800 break-all">
                      {order.product_id || "—"}
                    </div>
                  </div>

                  <div className="flex justify-between items-center">
                    <div>
                      <p className="text-lg font-bold text-gray-900">
                        Total: ${total.toFixed(2)}
                      </p>
                    </div>

                    <button
                      className="px-4 py-2 bg-black text-white rounded-lg hover:opacity-90"
                      disabled={!id}
                      onClick={() => nav(`/my-orders/${id}`)}
                    >
                      View Details
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-12 bg-white rounded-lg shadow-md">
            <p className="text-gray-500 text-lg">No orders found</p>
            <p className="text-gray-400">Start shopping to create your first order</p>
          </div>
        )}
      </div>
    </Container>
  );
}
