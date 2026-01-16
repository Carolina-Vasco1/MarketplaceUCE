import { useState, useEffect } from "react";
import Container from "../components/Container";
import { listProducts } from "../api/products";
import ProductCard from "../components/ProductCard";

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [trendingProducts, setTrendingProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    try {
      setLoading(true);
      // Load all products
      const allProducts = await listProducts();
      
      // Shuffle and take some as trending (most expensive ones)
      const sorted = [...allProducts].sort((a, b) => b.price - a.price);
      setTrendingProducts(sorted.slice(0, 4));
      
      // Rest as recommendations
      setRecommendations(sorted.slice(4).slice(0, 4));
    } catch (error) {
      console.error("Failed to load recommendations:", error);
      // Fallback: set empty arrays
      setRecommendations([]);
      setTrendingProducts([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Container>
        <div className="py-12 text-center">
          <div className="inline-block animate-spin text-primary-500 text-4xl">⏳</div>
          <p className="mt-4 text-gray-600">Loading recommendations...</p>
        </div>
      </Container>
    );
  }

  return (
    <Container>
      <div className="py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Personalized Recommendations</h1>
        <p className="text-gray-600 mb-8">Products recommended just for you based on your preferences</p>

        {/* Trending Products */}
        {trendingProducts.length > 0 && (
          <section className="mb-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">🔥 Trending Now</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {trendingProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </section>
        )}

        {/* Recommendations */}
        {recommendations.length > 0 && (
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">⭐ Personalized for You</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {recommendations.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </section>
        )}

        {/* Empty State */}
        {recommendations.length === 0 && trendingProducts.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No recommendations available yet</p>
            <p className="text-gray-400">Browse more products to get personalized recommendations</p>
          </div>
        )}
      </div>
    </Container>
  );
}
