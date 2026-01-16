import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import Container from "../components/Container";
import { useCart } from "../store/cartStore";

interface CheckoutForm {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  zipCode: string;
  country: string;
}

type PayPalConfig = {
  client_id: string;
  environment: "sandbox" | "production";
};

export default function CartPage() {
  const { items, removeItem, updateQuantity, clearCart, getTotalPrice } = useCart();
  const navigate = useNavigate();

  const [showCheckout, setShowCheckout] = useState(false);
  const [paypalReady, setPaypalReady] = useState(false);
  const [paypalError, setPaypalError] = useState<string | null>(null);
  const [paypalConfig, setPaypalConfig] = useState<PayPalConfig | null>(null);

  const renderedRef = useRef(false);

  const [formData, setFormData] = useState<CheckoutForm>({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    address: "",
    city: "",
    zipCode: "",
    country: "EC",
  });

  // 1) Traer client_id desde gateway
  useEffect(() => {
    (async () => {
      try {
        const r = await fetch("http://localhost:8000/api/v1/config/paypal");
        if (!r.ok) throw new Error("No se pudo obtener config paypal");
        const data = (await r.json()) as PayPalConfig;

        if (!data.client_id) throw new Error("PAYPAL_CLIENT_ID vacío en gateway");

        setPaypalConfig(data);
      } catch (e: any) {
        setPaypalError(e.message || "Error cargando config PayPal");
      }
    })();
  }, []);

  // 2) Cargar SDK usando ese client_id
  useEffect(() => {
    if (!paypalConfig) return;

    const src = `https://www.paypal.com/sdk/js?client-id=${encodeURIComponent(
      paypalConfig.client_id
    )}&currency=USD&intent=capture`;

    // si ya existe el script, no lo dupliques
    const existing = document.querySelector(`script[src="${src}"]`);
    if (existing) {
      setPaypalReady(true);
      return;
    }

    const script = document.createElement("script");
    script.src = src;
    script.async = true;

    script.onload = () => {
      setPaypalReady(true);
    };
    script.onerror = () => {
      setPaypalError("No se pudo cargar el SDK de PayPal (revisa client-id / adblock / internet).");
    };

    document.head.appendChild(script);
  }, [paypalConfig]);

  // 3) Render botones cuando ya estás en checkout
  useEffect(() => {
    if (!showCheckout) return;
    if (!paypalReady) return;
    if (!window.paypal?.Buttons) return;

    // evita render doble (React strict mode)
    if (renderedRef.current) return;
    renderedRef.current = true;

    const containerId = "#paypal-button-container";
    const total = getTotalPrice() + getTotalPrice() * 0.1;

    try {
      window.paypal
        .Buttons({
          createOrder: (_data: any, actions: any) => {
            return actions.order.create({
              purchase_units: [
                {
                  amount: {
                    currency_code: "USD",
                    value: total.toFixed(2),
                  },
                },
              ],
            });
          },
          onApprove: async (_data: any, actions: any) => {
            const order = await actions.order.capture();

            // ✅ Llama a tu backend usando GATEWAY (no relativo)
            const res = await fetch("http://localhost:8000/order/api/v1/orders/create-from-cart", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                paypal_order_id: order.id,
                items: items.map((i) => ({
                  product_id: i.id,
                  quantity: i.quantity,
                  price: i.price,
                })),
                customer: formData,
                total_price: total,
                payment_status: "completed",
                created_at: new Date().toISOString(),
              }),
            });

            if (!res.ok) throw new Error("No se pudo crear la orden en backend");

            clearCart();
            alert("Pago aprobado (SANDBOX) ✅");
            navigate("/orders");
          },
          onError: (err: any) => {
            console.error(err);
            setPaypalError("Error de PayPal. Revisa consola.");
          },
        })
        .render(containerId);
    } catch (e: any) {
      setPaypalError(e.message || "Error renderizando PayPal");
    }
  }, [showCheckout, paypalReady]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((p) => ({ ...p, [name]: value }));
  };

  if (items.length === 0 && !showCheckout) {
    return (
      <Container>
        <div className="text-center py-12">
          <h1 className="text-3xl font-bold mb-4">Shopping Cart</h1>
          <p className="text-gray-600 mb-6">Your cart is empty</p>
          <button onClick={() => navigate("/")} className="bg-black text-white px-6 py-2 rounded-lg">
            Continue Shopping
          </button>
        </div>
      </Container>
    );
  }

  return (
    <Container>
      <h1 className="text-3xl font-bold mb-6">Shopping Cart</h1>

      {paypalError && (
        <div className="mb-4 p-3 border border-red-300 bg-red-50 text-red-800 rounded">
          {paypalError}
        </div>
      )}

      {/* ...tu UI igual... */}

      {/* PayPal */}
      {showCheckout && (
        <div className="mb-6 p-4 bg-gray-50 border-2 border-gray-200 rounded-lg min-h-60 flex items-center justify-center">
          {paypalReady ? (
            <div id="paypal-button-container" className="w-full"></div>
          ) : (
            <div className="text-blue-800">Loading PayPal... Please wait</div>
          )}
        </div>
      )}

      {/* botón checkout */}
      {!showCheckout ? (
        <button
          onClick={() => {
            renderedRef.current = false; // reset para render
            setShowCheckout(true);
          }}
          className="w-full bg-black text-white py-3 rounded-lg font-semibold"
        >
          Checkout
        </button>
      ) : (
        <button
          onClick={() => {
            renderedRef.current = false;
            setShowCheckout(false);
          }}
          className="w-full border py-3 rounded-lg font-semibold"
        >
          Back to Cart
        </button>
      )}
    </Container>
  );
}

declare global {
  interface Window {
    paypal?: any;
  }
}
