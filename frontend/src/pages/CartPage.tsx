import { useEffect, useState } from "react";
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

export default function CartPage() {
  const { items, removeItem, updateQuantity, clearCart, getTotalPrice } =
    useCart();
  const navigate = useNavigate();
  const [processing, setProcessing] = useState(false);
  const [showCheckout, setShowCheckout] = useState(false);
  const [paypalReady, setPaypalReady] = useState(false);
  const [formData, setFormData] = useState<CheckoutForm>({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    address: "",
    city: "",
    zipCode: "",
    country: "",
  });

  useEffect(() => {
    // Load PayPal script with client-id from backend
    if (document.querySelector('script[src*="paypal.com/sdk/js"]')) {
      // Script already loaded
      setPaypalReady(true);
      return;
    }

    const loadPayPalScript = async () => {
      try {
        // Get PayPal client-id from backend
        const configResponse = await fetch("/api/v1/config/paypal");
        const config = await configResponse.json();
        
        const script = document.createElement("script");
        script.src = `https://www.paypal.com/sdk/js?client-id=${config.client_id}&currency=USD`;
        script.async = true;
        script.onload = () => {
          console.log("✅ PayPal SDK loaded successfully");
          setPaypalReady(true);
        };
        script.onerror = () => {
          console.error("❌ Failed to load PayPal SDK");
        };
        document.head.appendChild(script);
      } catch (error) {
        console.error("❌ Failed to get PayPal config:", error);
      }
    };

    loadPayPalScript();

    return () => {
      // Cleanup: remove script if component unmounts
      const existingScript = document.querySelector(
        'script[src*="paypal.com/sdk/js"]'
      );
      if (existingScript) {
        existingScript.remove();
      }
    };
  }, []);

  useEffect(() => {
    if (showCheckout && paypalReady) {
      console.log("🔄 Checkout view shown, PayPal ready. Waiting for DOM...");
      // Increase delay to ensure DOM is fully rendered
      setTimeout(() => {
        const container = document.getElementById("paypal-button-container");
        console.log("🔍 Looking for PayPal container:", !!container);
        console.log("🔍 window.paypal exists:", !!window.paypal);
        
        if (container && window.paypal?.Buttons) {
          console.log("✅ All conditions met, initializing PayPal buttons");
          initPayPalButtons();
        } else {
          console.warn("⚠️ Conditions not met. Container:", !!container, "window.paypal:", !!window.paypal);
        }
      }, 500);
    }
  }, [showCheckout, paypalReady]);

  const initPayPalButtons = async () => {
    const container = document.getElementById("paypal-button-container");
    
    if (!container) {
      console.error("PayPal container not found");
      return;
    }

    if (!window.paypal) {
      console.error("window.paypal not available");
      return;
    }

    if (!window.paypal.Buttons) {
      console.error("window.paypal.Buttons not available");
      return;
    }

    console.log("Starting PayPal button initialization");
    
    // Clear any existing content
    container.innerHTML = "";

    try {
      const buttonsInstance = window.paypal.Buttons({
        createOrder: async (data: any, actions: any) => {
          console.log("Creating PayPal order");
          const total = getTotalPrice() + getTotalPrice() * 0.1;
          return actions.order.create({
            purchase_units: [
              {
                amount: {
                  value: total.toFixed(2),
                  breakdown: {
                    item_total: {
                      currency_code: "USD",
                      value: getTotalPrice().toFixed(2),
                    },
                    tax_total: {
                      currency_code: "USD",
                      value: (getTotalPrice() * 0.1).toFixed(2),
                    },
                  },
                },
                items: items.map((item) => ({
                  name: item.title,
                  quantity: item.quantity.toString(),
                  unit_amount: {
                    currency_code: "USD",
                    value: item.price.toFixed(2),
                  },
                })),
              },
            ],
            payer: {
              name: {
                given_name: formData.firstName,
                surname: formData.lastName,
              },
              email_address: formData.email,
              address: {
                address_line_1: formData.address,
                admin_area_2: formData.city,
                postal_code: formData.zipCode,
                country_code: formData.country,
              },
            },
          });
        },
        onApprove: async (data: any, actions: any) => {
          try {
            console.log("Payment approved, capturing order");
            const order = await actions.order.capture();
            console.log("Payment successful:", order);

            // Send order to backend
            const orderData = {
              paypal_order_id: order.id,
              items: items.map((item) => ({
                product_id: item.id,
                quantity: item.quantity,
                price: item.price,
              })),
              customer: formData,
              total_price: getTotalPrice() + getTotalPrice() * 0.1,
              payment_status: "completed",
              created_at: new Date().toISOString(),
            };

            // Call backend to save order
            const response = await fetch("/order/api/v1/orders/create-from-cart", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(orderData),
            });

            if (response.ok) {
              clearCart();
              alert("Payment successful! Your order has been placed.");
              navigate("/orders");
            } else {
              throw new Error("Failed to create order");
            }
          } catch (error) {
            console.error("Payment capture error:", error);
            alert("Payment failed. Please try again.");
          }
        },
        onError: (error: any) => {
          console.error("PayPal error:", error);
          alert("Payment error. Please try again.");
        },
      });

      console.log("Rendering PayPal buttons");
      buttonsInstance.render("#paypal-button-container");
      console.log("PayPal buttons rendered successfully");
    } catch (error) {
      console.error("Error creating PayPal buttons:", error);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const validateForm = () => {
    if (
      !formData.firstName ||
      !formData.lastName ||
      !formData.email ||
      !formData.address
    ) {
      alert("Please fill in all required fields");
      return false;
    }
    return true;
  };

  if (items.length === 0 && !showCheckout) {
    return (
      <Container>
        <div className="text-center py-12">
          <h1 className="text-3xl font-bold mb-4">🛒 Shopping Cart</h1>
          <p className="text-gray-600 mb-6">Your cart is empty</p>
          <button
            onClick={() => navigate("/")}
            className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-2 rounded-lg"
          >
            Continue Shopping
          </button>
        </div>
      </Container>
    );
  }

  return (
    <Container>
      <h1 className="text-3xl font-bold mb-6">🛒 Shopping Cart</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Cart Items */}
        <div className="lg:col-span-2">
          {!showCheckout ? (
            <div className="space-y-4">
              {items.map((item) => (
                <div
                  key={item.id}
                  className="border rounded-lg p-4 flex gap-4 items-center bg-white shadow-sm hover:shadow-md transition"
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
                      onClick={() =>
                        updateQuantity(item.id, Math.max(1, item.quantity - 1))
                      }
                      className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 font-semibold"
                    >
                      −
                    </button>
                    <span className="w-8 text-center font-semibold">
                      {item.quantity}
                    </span>
                    <button
                      onClick={() =>
                        updateQuantity(item.id, item.quantity + 1)
                      }
                      className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 font-semibold"
                    >
                      +
                    </button>
                  </div>
                  <button
                    onClick={() => removeItem(item.id)}
                    className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded transition"
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          ) : (
            // Checkout Form
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <h2 className="text-2xl font-bold mb-6">Billing Information</h2>
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <label className="block text-sm font-semibold mb-2">
                    First Name *
                  </label>
                  <input
                    type="text"
                    name="firstName"
                    placeholder="John"
                    value={formData.firstName}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold mb-2">
                    Last Name *
                  </label>
                  <input
                    type="text"
                    name="lastName"
                    placeholder="Doe"
                    value={formData.lastName}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <label className="block text-sm font-semibold mb-2">
                    Email *
                  </label>
                  <input
                    type="email"
                    name="email"
                    placeholder="john@example.com"
                    value={formData.email}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold mb-2">
                    Phone
                  </label>
                  <input
                    type="tel"
                    name="phone"
                    placeholder="+1 234 567 8900"
                    value={formData.phone}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-semibold mb-2">
                  Address *
                </label>
                <input
                  type="text"
                  name="address"
                  placeholder="123 Main Street"
                  value={formData.address}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  required
                />
              </div>

              <div className="grid grid-cols-3 gap-4 mb-6">
                <div>
                  <label className="block text-sm font-semibold mb-2">
                    City
                  </label>
                  <input
                    type="text"
                    name="city"
                    placeholder="New York"
                    value={formData.city}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold mb-2">
                    ZIP Code
                  </label>
                  <input
                    type="text"
                    name="zipCode"
                    placeholder="10001"
                    value={formData.zipCode}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold mb-2">
                    Country
                  </label>
                  <select
                    name="country"
                    value={formData.country}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="">Select...</option>
                    <option value="US">United States</option>
                    <option value="CA">Canada</option>
                    <option value="GB">United Kingdom</option>
                    <option value="AU">Australia</option>
                    <option value="DE">Germany</option>
                    <option value="FR">France</option>
                    <option value="JP">Japan</option>
                    <option value="MX">Mexico</option>
                    <option value="EC">Ecuador</option>
                    <option value="CO">Colombia</option>
                    <option value="PE">Peru</option>
                    <option value="CL">Chile</option>
                    <option value="AR">Argentina</option>
                    <option value="BR">Brazil</option>
                    <option value="ES">Spain</option>
                    <option value="IT">Italy</option>
                    <option value="NL">Netherlands</option>
                    <option value="BE">Belgium</option>
                    <option value="CH">Switzerland</option>
                    <option value="SE">Sweden</option>
                    <option value="NO">Norway</option>
                    <option value="DK">Denmark</option>
                    <option value="FI">Finland</option>
                    <option value="PL">Poland</option>
                    <option value="CZ">Czech Republic</option>
                    <option value="HU">Hungary</option>
                    <option value="RO">Romania</option>
                    <option value="GR">Greece</option>
                    <option value="PT">Portugal</option>
                    <option value="TR">Turkey</option>
                    <option value="SG">Singapore</option>
                    <option value="MY">Malaysia</option>
                    <option value="TH">Thailand</option>
                    <option value="ID">Indonesia</option>
                    <option value="PH">Philippines</option>
                    <option value="VN">Vietnam</option>
                    <option value="KR">South Korea</option>
                    <option value="CN">China</option>
                    <option value="IN">India</option>
                    <option value="ZA">South Africa</option>
                    <option value="EG">Egypt</option>
                    <option value="NG">Nigeria</option>
                  </select>
                </div>
              </div>

              {/* PayPal Button Container */}
              {paypalReady ? (
                <div className="mb-6 p-4 bg-gray-50 border-2 border-gray-200 rounded-lg min-h-60 flex items-center justify-center">
                  <div id="paypal-button-container" className="w-full"></div>
                </div>
              ) : (
                <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
                  <p className="text-blue-800">Loading PayPal... Please wait</p>
                </div>
              )}

              <div className="flex gap-4">
                <button
                  onClick={() => setShowCheckout(false)}
                  className="flex-1 px-6 py-2 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition"
                >
                  Back to Cart
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Summary */}
        <div className="bg-gray-50 rounded-lg p-6 h-fit sticky top-6">
          <h2 className="text-xl font-bold mb-4">Order Summary</h2>

          {/* Items in summary */}
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
              <span className="font-semibold">
                ${getTotalPrice().toFixed(2)}
              </span>
            </div>
            <div className="flex justify-between">
              <span>Shipping:</span>
              <span className="font-semibold text-green-600">Free</span>
            </div>
            <div className="flex justify-between">
              <span>Tax (10%):</span>
              <span className="font-semibold">
                ${(getTotalPrice() * 0.1).toFixed(2)}
              </span>
            </div>
            <div className="border-t pt-3 flex justify-between font-bold text-lg">
              <span>Total:</span>
              <span className="text-primary-600">
                ${(getTotalPrice() + getTotalPrice() * 0.1).toFixed(2)}
              </span>
            </div>
          </div>

          {!showCheckout ? (
            <button
              onClick={() => setShowCheckout(true)}
              className="w-full bg-primary-500 hover:bg-primary-600 text-white py-3 rounded-lg font-semibold transition"
            >
              💳 Checkout
            </button>
          ) : (
            <div className="space-y-2">
              <p className="text-sm text-gray-600">
                Secure payment powered by PayPal
              </p>
              <div className="bg-blue-50 border border-blue-200 rounded p-3">
                <p className="text-sm font-semibold text-blue-900">
                  Total to Pay: $
                  {(getTotalPrice() + getTotalPrice() * 0.1).toFixed(2)}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </Container>
  );
}

declare global {
  interface Window {
    paypal?: any;
  }
}
