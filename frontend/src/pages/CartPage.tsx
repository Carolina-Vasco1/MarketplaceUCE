import { useEffect, useState } from "react";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";
import { api } from "../api/http"; // tu axios

export default function CartPage() {
  const [clientId, setClientId] = useState<string>("");

  useEffect(() => {
    (async () => {
      const r = await api.get("/api/v1/config/paypal");
      setClientId(r.data.client_id);
    })();
  }, []);

  if (!clientId) return <div>Loading PayPal... Please wait</div>;

  return (
    <PayPalScriptProvider options={{ "client-id": clientId, currency: "USD", intent: "capture" }}>
      <PayPalButtons
        style={{ layout: "vertical" }}
        createOrder={async () => {
          // aquí llamas a tu backend payment-service (a través del gateway) para crear la orden
          const res = await api.post("/payment/api/v1/paypal/create-order", { total: 27.5 });
          return res.data.id; // id de la orden de PayPal
        }}
        onApprove={async (data) => {
          await api.post("/payment/api/v1/paypal/capture-order", { order_id: data.orderID });
          alert("Pago aprobado (sandbox)");
        }}
      />
    </PayPalScriptProvider>
  );
}
