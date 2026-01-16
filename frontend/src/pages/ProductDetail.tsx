import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Container from "../components/Container";
import type { Product } from "../types/models";
import { getProduct } from "../api/products";
import { useCart } from "../store/cartStore";

export default function ProductDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addItem } = useCart();
  const [p, setP] = useState<Product | null>(null);
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [addedToCart, setAddedToCart] = useState(false);

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

  const handleAddToCart = () => {
    if (!p) return;
    
    const img = p.images?.[0];
    addItem({
      id: p.id,
      title: p.title,
      price: p.price,
      quantity: quantity,
      image_url: img ? `http://localhost:8000${img}` : undefined,
    });
    
    setAddedToCart(true);
    setTimeout(() => setAddedToCart(false), 2000);
  };

  useEffect(() => {
    load();
  }, [id]);

  if (loading) {
    return (
      <Container>
        <div className="py-12 text-center">
          <div className="inline-block animate-spin text-primary-500 text-4xl">⏳</div>
          <p className="mt-4 text-gray-600">Loading product...</p>
        </div>
      </Container>
    );
  }

  if (err) {
    return (
      <Container>
        <div className="py-12 text-center">
          <p className="text-red-600 text-lg mb-4">{err}</p>
          <button
            onClick={() => navigate("/")}
            className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-2 rounded-lg"
          >
            Back to Home
          </button>
        </div>
      </Container>
    );
  }

  if (!p) {
    return (
      <Container>
        <div className="py-12 text-center">
          <p className="text-gray-600">Product not found</p>
        </div>
      </Container>
    );
  }

  const img = p.images?.[0];
  const rating = p.rating || 4.5;
  const reviewCount = p.review_count || Math.floor(Math.random() * 100);

  return (
    <Container>
      <div className="py-8">
        <button
          onClick={() => navigate(-1)}
          className="text-primary-500 hover:text-primary-600 mb-6 font-semibold"
        >
          ← Back
        </button>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Product Image */}
          <div className="bg-gray-100 rounded-lg overflow-hidden h-96">
            {img ? (
              <img
                src={`http://localhost:8000${img}`}
                alt={p.title}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-gray-400 text-6xl">
                📦
              </div>
            )}
          </div>

          {/* Product Details */}
          <div className="space-y-6">
            {/* Title and Price */}
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">{p.title}</h1>
              <div className="flex items-center gap-2 mb-4">
                <div className="flex text-yellow-400">
                  {"⭐".repeat(Math.floor(rating))}
                </div>
                <span className="text-sm text-gray-600">
                  {rating.toFixed(1)} ({reviewCount} reviews)
                </span>
              </div>
            </div>

            {/* Price */}
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-gray-600 text-sm">Price</p>
              <p className="text-4xl font-bold text-primary-600">
                ${p.price.toFixed(2)}
              </p>
            </div>

            {/* Description */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Description</h3>
              <p className="text-gray-700 leading-relaxed">{p.description}</p>
            </div>

            {/* Product Info */}
            <div className="grid grid-cols-2 gap-4 border-t border-b py-4">
              <div>
                <p className="text-sm text-gray-600">Category</p>
                <p className="font-semibold text-gray-900">
                  {p.category || "Not specified"}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Stock</p>
                <p className="font-semibold text-gray-900">
                  {(p.stock ?? 1) > 0 ? "In Stock" : "Out of Stock"}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Seller</p>
                <p className="font-semibold text-gray-900">
                  {p.seller_name || "Unknown"}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Seller Email</p>
                <p className="font-semibold text-gray-900 text-sm">
                  {p.seller_id || "-"}
                </p>
              </div>
            </div>

            {/* Quantity and Add to Cart */}
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <label className="text-gray-900 font-semibold">Quantity:</label>
                <div className="flex items-center border border-gray-300 rounded-lg">
                  <button
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    className="px-4 py-2 text-gray-600 hover:bg-gray-100"
                  >
                    −
                  </button>
                  <input
                    type="number"
                    value={quantity}
                    onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                    className="w-16 text-center border-0 py-2 focus:outline-none"
                    min="1"
                  />
                  <button
                    onClick={() => setQuantity(quantity + 1)}
                    className="px-4 py-2 text-gray-600 hover:bg-gray-100"
                  >
                    +
                  </button>
                </div>
              </div>

              <button
                onClick={handleAddToCart}
                disabled={(p.stock ?? 1) <= 0}
                className={`w-full py-3 rounded-lg font-semibold text-white transition ${
                  (p.stock ?? 1) <= 0
                    ? "bg-gray-400 cursor-not-allowed"
                    : "bg-primary-500 hover:bg-primary-600"
                }`}
              >
                {addedToCart ? "✓ Added to Cart!" : "🛒 Add to Cart"}
              </button>

              <button
                onClick={() => navigate("/cart")}
                className="w-full py-2 border-2 border-primary-500 text-primary-500 rounded-lg font-semibold hover:bg-primary-50"
              >
                View Cart
              </button>
            </div>
          </div>
        </div>
      </div>
    </Container>
  );
}
