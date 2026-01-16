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

declare global {
  interface Window {
    paypal?: any;
  }
}

export default function CartPage() {
  const { items, removeItem, updateQuantity, clearCart, getTotalPrice } = useCart();
  const navigate = useNavigate();

  const [showCheckout, setShowCheckout] = useState(false);

  const [paypalConfig, setPaypalConfig] = useState<PayPalConfig | null>(null);
  const [paypalReady, setPaypalReady] = useState(false);
  const [paypalError, setPaypalError] = useState<string | null>(null);

  // refs para evitar stale-closure + re-render innecesario del SDK
  const renderedRef = useRef(false);
  const itemsRef = useRef(items);
  const formRef = useRef<CheckoutForm>({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    address: "",
    city: "",
    zipCode: "",
    country: "EC",
  });

  const [formData, setFormData] = useState<CheckoutForm>(formRef.current);

  useEffect(() => {
    itemsRef.current = items;
  }, [items]);

  useEffect(() => {
    formRef.current = formData;
  }, [formData]);

  // 1) Traer config PayPal desde gateway
  useEffect(() => {
    (async () => {
      try {
        const r = await fetch("http://localhost:8000/api/v1/config/paypal");
        if (!r.ok) throw new Error("No se pudo obtener config PayPal (gateway)");
        const data = (await r.json()) as PayPalConfig;

        if (!data.client_id) throw new Error("PAYPAL_CLIENT_ID vacío en el backend");
        setPaypalConfig(data);
      } catch (e: any) {
        setPaypalError(e?.message || "Error cargando config PayPal");
      }
    })();
  }, []);

  // 2) Cargar SDK PayPal usando client_id dinámico
  useEffect(() => {
    if (!paypalConfig) return;

    // OJO: en sandbox normalmente el client_id empieza con "AY..." o similar.
    // Da igual: si el client_id es sandbox, funcionará en sandbox.
    const src = `https://www.paypal.com/sdk/js?client-id=${encodeURIComponent(
      paypalConfig.client_id
    )}&currency=USD&intent=capture`;

    // si ya existe el script, no dupliques
    const existingAny = document.querySelector('script[src*="paypal.com/sdk/js"]') as HTMLScriptElement | null;
    if (existingAny) {
      // si el script existente es de otro client_id, lo removemos para evitar conflicto
      if (existingAny.src !== src) existingAny.remove();
      else {
        setPaypalReady(true);
        return;
      }
    }

    setPaypalReady(false);
    setPaypalError(null);

    const script = document.createElement("script");
    script.src = src;
    script.async = true;

    script.onload = () => setPaypalReady(true);
    script.onerror = () => setPaypalError("No se pudo cargar el SDK de PayPal (adblock / client-id / internet).");

    document.head.appendChild(script);
  }, [paypalConfig]);

  // 3) Render de botones cuando estás en checkout
  useEffect(() => {
    if (!showCheckout) return;
    if (!paypalReady) return;
    if (!window.paypal?.Buttons) return;

    // evita doble render por StrictMode o re-renders
    if (renderedRef.current) return;
    renderedRef.current = true;

    const container = document.getElementById("paypal-button-container");
    if (!container) return;
    container.innerHTML = "";

    const subtotal = getTotalPrice();
    const tax = subtotal * 0.1;
    const total = subtotal + tax;

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
                    breakdown: {
                      item_total: { currency_code: "USD", value: subtotal.toFixed(2) },
                      tax_total: { currency_code: "USD", value: tax.toFixed(2) },
                    },
                  },
                  items: itemsRef.current.map((i) => ({
                    name: i.title,
                    quantity: String(i.quantity),
                    unit_amount: { currency_code: "USD", value: i.price.toFixed(2) },
                  })),
                },
              ],
            });
          },

          onApprove: async (_data: any, actions: any) => {
            try {
              const order = await actions.order.capture();

              const payload = {
                paypal_order_id: order.id,
                items: itemsRef.current.map((i) => ({
                  product_id: i.id,
                  quantity: i.quantity,
                  price: i.price,
                })),
                customer: formRef.current,
                total_price: total,
                payment_status: "completed",
                created_at: new Date().toISOString(),
              };

              // IMPORTANTE: usa el gateway, no relativo
              const res = await fetch("http://localhost:8000/order/api/v1/orders/create-from-cart", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
              });

              if (!res.ok) throw new Error("No se pudo crear la orden en backend");

              clearCart();
              alert("Pago aprobado (SANDBOX) ✅");
              // En tu App.tsx el path es /my-orders
              navigate("/my-orders");
            } catch (e: any) {
              console.error(e);
              setPaypalError(e?.message || "Error capturando pago/creando orden");
            }
          },

          onError: (err: any) => {
            console.error(err);
            setPaypalError("Error de PayPal. Revisa consola.");
          },
        })
        .render("#paypal-button-container");
    } catch (e: any) {
      setPaypalError(e?.message || "Error renderizando botones PayPal");
    }
  }, [showCheckout, paypalReady, getTotalPrice, clearCart, navigate]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((p) => ({ ...p, [name]: value }));
  };

  // Si no hay items y no estás en checkout
  if (items.length === 0 && !showCheckout) {
    return (
      <Container>
        <div className="text-center py-12">
          <h1 className="text-3xl font-bold mb-4">Shopping Cart</h1>
          <p className="text-gray-600 mb-6">Your cart is empty</p>
          <button
            onClick={() => navigate("/")}
            className="bg-black text-white px-6 py-2 rounded-lg"
          >
            Continue Shopping
          </button>
        </div>
      </Container>
    );
  }

  const subtotal = getTotalPrice();
  const tax = subtotal * 0.1;
  const total = subtotal + tax;

  return (
    <Container>
      <h1 className="text-3xl font-bold mb-6">Shopping Cart</h1>

      {paypalError && (
        <div className="mb-4 p-3 border border-red-300 bg-red-50 text-red-800 rounded">
          {paypalError}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* LEFT */}
        <div className="lg:col-span-2">
          {!showCheckout ? (
            <div className="space-y-4">
              {items.map((item) => (
                <div
                  key={item.id}
                  className="border rounded-lg p-4 flex gap-4 items-center bg-white shadow-sm"
                >
                  {item.image_url && (
                    <img
                      src={item.image_url}
                      alt={item.title}
                      className="w-24 h-24 object-cover rounded"
                    />
                  )}

                  <div className="flex-1">
                    <h3 className="font-semibold text-lg">{item.title}</h3>
                    <p className="text-gray-600">${item.price.toFixed(2)}</p>
                    <p className="text-sm text-gray-500 mt-1">
                      Subtotal: ${(item.price * item.quantity).toFixed(2)}
                    </p>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => updateQuantity(item.id, Math.max(1, item.quantity - 1))}
                      className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 font-semibold"
                    >
                      −
                    </button>
                    <span className="w-8 text-center font-semibold">{item.quantity}</span>
                    <button
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                      className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 font-semibold"
                    >
                      +
                    </button>
                  </div>

                  <button
                    onClick={() => removeItem(item.id)}
                    className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded"
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <h2 className="text-2xl font-bold mb-6">Billing Information</h2>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <label className="block text-sm font-semibold mb-2">First Name *</label>
                  <input
                    type="text"
                    name="firstName"
                    value={formData.firstName}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border rounded-lg"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold mb-2">Last Name *</label>
                  <input
                    type="text"
                    name="lastName"
                    value={formData.lastName}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border rounded-lg"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <label className="block text-sm font-semibold mb-2">Email *</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border rounded-lg"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold mb-2">Phone</label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border rounded-lg"
                  />
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-semibold mb-2">Address *</label>
                <input
                  type="text"
                  name="address"
                  value={formData.address}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border rounded-lg"
                  required
                />
              </div>

              <div className="grid grid-cols-3 gap-4 mb-6">
                <div>
                  <label className="block text-sm font-semibold mb-2">City</label>
                  <input
                    type="text"
                    name="city"
                    value={formData.city}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold mb-2">ZIP Code</label>
                  <input
                    type="text"
                    name="zipCode"
                    value={formData.zipCode}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold mb-2">Country</label>
                  <select
                    name="country"
                    value={formData.country}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border rounded-lg"
                  >
                    <option value="EC">Ecuador</option>
                    <option value="US">United States</option>
                    <option value="CO">Colombia</option>
                    <option value="PE">Peru</option>
                  </select>
                </div>
              </div>

              <div className="mb-6 p-4 bg-gray-50 border-2 border-gray-200 rounded-lg min-h-60 flex items-center justify-center">
                {paypalReady ? (
                  <div id="paypal-button-container" className="w-full" />
                ) : (
                  <div className="text-blue-800">Loading PayPal... Please wait</div>
                )}
              </div>

              <button
                onClick={() => {
                  renderedRef.current = false;
                  setShowCheckout(false);
                }}
                className="w-full border py-3 rounded-lg font-semibold"
              >
                Back to Cart
              </button>
            </div>
          )}
        </div>

        {/* RIGHT SUMMARY */}
        <div className="bg-gray-50 rounded-lg p-6 h-fit sticky top-6">
          <h2 className="text-xl font-bold mb-4">Order Summary</h2>

          <div className="mb-4 pb-4 border-b max-h-48 overflow-y-auto">
            {items.map((item) => (
              <div key={item.id} className="flex justify-between text-sm mb-2">
                <span>
                  {item.title} x{item.quantity}
                </span>
                <span className="font-semibold">
                  ${(item.price * item.quantity).toFixed(2)}
                </span>
              </div>
            ))}
          </div>

          <div className="space-y-3 mb-6">
            <div className="flex justify-between">
              <span>Subtotal:</span>
              <span className="font-semibold">${subtotal.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span>Shipping:</span>
              <span className="font-semibold text-green-600">Free</span>
            </div>
            <div className="flex justify-between">
              <span>Tax (10%):</span>
              <span className="font-semibold">${tax.toFixed(2)}</span>
            </div>
            <div className="border-t pt-3 flex justify-between font-bold text-lg">
              <span>Total:</span>
              <span>${total.toFixed(2)}</span>
            </div>
          </div>

          {!showCheckout ? (
            <button
              onClick={() => {
                renderedRef.current = false;
                setShowCheckout(true);
              }}
              className="w-full bg-black text-white py-3 rounded-lg font-semibold"
            >
              Checkout
            </button>
          ) : (
            <div className="text-sm text-gray-600">
              Secure payment powered by PayPal
            </div>
          )}
        </div>
      </div>
    </Container>
  );
}
