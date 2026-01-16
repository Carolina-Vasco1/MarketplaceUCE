import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Container from "../components/Container";
import ProductCard from "../components/ProductCard";
import type { Product } from "../types/models";
import { listProducts } from "../api/products";
import { aiAPI } from "../api/ai";

export default function Marketplace() {
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<Product[]>([]);
  const [featured, setFeatured] = useState<Product[]>([]);
  const [err, setErr] = useState("");

  async function load() {
    setErr("");
    setLoading(true);
    try {
      const data = await listProducts();
      setItems(data);
      // Featured products are the first 4
      setFeatured(data.slice(0, 4));
    } catch (e: any) {
      setErr(
        e?.response?.data?.detail ??
          "Unable to load products (check gateway/backend)."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <Container>
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-500 to-secondary-600 rounded-lg shadow-lg p-12 mb-12 text-white">
        <div className="max-w-2xl">
          <h1 className="text-5xl font-bold mb-4">Welcome to Marketplace UCE</h1>
          <p className="text-lg opacity-90 mb-6">
            Discover amazing products from verified sellers. Shop smart, save big.
          </p>
          <div className="flex gap-4">
            <Link
              to="/search"
              className="px-6 py-3 bg-white text-primary-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors"
            >
              🔍 Search Products
            </Link>
            <Link
              to="/recommendations"
              className="px-6 py-3 border-2 border-white text-white font-semibold rounded-lg hover:bg-white/10 transition-colors"
            >
              ⭐ Get Recommendations
            </Link>
          </div>
        </div>
      </div>

      {/* Featured Products */}
      {featured.length > 0 && (
        <div className="mb-12">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-3xl font-bold text-gray-900">🔥 Trending Now</h2>
              <p className="text-gray-600">Hot deals this week</p>
            </div>
            <Link
              to="/recommendations"
              className="text-primary-600 hover:text-primary-700 font-semibold"
            >
              View All →
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {featured.map((p) => (
              <ProductCard key={p.id} p={p} />
            ))}
          </div>
        </div>
      )}

      {/* All Products Section */}
      <div className="mb-8">
        <div className="flex items-center justify-between gap-3 flex-wrap mb-6">
          <div>
            <h2 className="text-3xl font-bold text-gray-900">All Products</h2>
            <p className="text-gray-600">
              Browse our complete catalog
            </p>
          </div>
          <button
            className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 font-semibold transition-colors"
            onClick={load}
          >
            🔄 Refresh
          </button>
        </div>

        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin text-primary-500 text-4xl">⏳</div>
            <p className="mt-4 text-gray-600">Loading products...</p>
          </div>
        )}

        {err && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
            <p className="font-semibold">Error loading products</p>
            <p className="text-sm mt-1">{err}</p>
          </div>
        )}

        {!loading && !err && (
          <div>
            {items.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {items.map((p) => (
                  <ProductCard key={p.id} p={p} />
                ))}
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-md p-12 text-center">
                <p className="text-gray-600 text-lg mb-4">📭 No products available yet</p>
                <p className="text-gray-500 mb-6">
                  If you are a seller, publish your first product to get started!
                </p>
                <Link
                  to="/sell"
                  className="inline-block px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 font-semibold transition-colors"
                >
                  Start Selling
                </Link>
              </div>
            )}
          </div>
        )}
      </div>

      {/* CTA Section */}
      {!loading && items.length > 0 && (
        <div className="bg-secondary-50 rounded-lg p-8 text-center border-2 border-secondary-200">
          <h3 className="text-2xl font-bold text-gray-900 mb-2">Have something to sell?</h3>
          <p className="text-gray-600 mb-4">
            Join thousands of successful sellers on our marketplace
          </p>
          <Link
            to="/sell"
            className="inline-block px-6 py-3 bg-secondary-600 text-white rounded-lg hover:bg-secondary-700 font-semibold transition-colors"
          >
            📦 Sell Your Products
          </Link>
        </div>
      )}
    </Container>
  );
}
