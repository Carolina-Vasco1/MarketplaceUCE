import { useState, useEffect } from "react";
import Container from "../components/Container";
import { reviewsAPI } from "../api/reviews";

export default function ReviewsPage() {
  const [products, setProducts] = useState<any[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<any>(null);
  const [formData, setFormData] = useState({ rating: 5, comment: "" });
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const prods = await reviewsAPI.getProductsForReview();
      setProducts((prods as any)?.products || prods?.data || prods);
    } catch (error) {
      console.error("Failed to load products:", error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedProduct) return;

    try {
      setLoading(true);
      await reviewsAPI.createReview({
        product_id: selectedProduct.id,
        rating: formData.rating,
        comment: formData.comment,
      });
      setSubmitted(true);
      setFormData({ rating: 5, comment: "" });
      setSelectedProduct(null);
      setTimeout(() => setSubmitted(false), 3000);
      loadProducts();
    } catch (error) {
      console.error("Failed to submit review:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <div className="py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Write a Review</h1>

        {submitted && (
          <div className="mb-6 p-4 bg-green-100 text-green-700 rounded-lg">
            ✅ Thank you! Your review has been submitted successfully.
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Product List */}
          <div className="lg:col-span-1">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Products</h2>
            <div className="space-y-2 bg-white rounded-lg shadow-md p-4">
              {products.map((product) => (
                <button
                  key={product.id}
                  onClick={() => setSelectedProduct(product)}
                  className={`w-full text-left p-3 rounded-lg transition-colors ${
                    selectedProduct?.id === product.id
                      ? "bg-primary-500 text-white"
                      : "bg-gray-100 hover:bg-gray-200"
                  }`}
                >
                  <p className="font-semibold">{product.name}</p>
                  <p className="text-sm opacity-75">${product.price}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Review Form */}
          <div className="lg:col-span-2">
            {selectedProduct ? (
              <div className="bg-white rounded-lg shadow-md p-8">
                <div className="mb-6">
                  <h3 className="text-2xl font-bold text-gray-900">
                    {selectedProduct.name}
                  </h3>
                  <p className="text-gray-600">${selectedProduct.price}</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* Rating */}
                  <div>
                    <label className="block text-lg font-semibold text-gray-900 mb-2">
                      Rating
                    </label>
                    <div className="flex gap-2 text-3xl">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <button
                          key={star}
                          type="button"
                          onClick={() => setFormData({ ...formData, rating: star })}
                          className={`cursor-pointer transition-colors ${
                            star <= formData.rating ? "text-yellow-400" : "text-gray-300"
                          }`}
                        >
                          ⭐
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Comment */}
                  <div>
                    <label className="block text-lg font-semibold text-gray-900 mb-2">
                      Comment
                    </label>
                    <textarea
                      value={formData.comment}
                      onChange={(e) =>
                        setFormData({ ...formData, comment: e.target.value })
                      }
                      placeholder="Share your experience with this product..."
                      className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none"
                    />
                  </div>

                  {/* Submit */}
                  <div className="flex gap-2">
                    <button
                      type="submit"
                      disabled={loading}
                      className="px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 font-semibold transition-colors"
                    >
                      {loading ? "Submitting..." : "Submit Review"}
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setSelectedProduct(null);
                        setFormData({ rating: 5, comment: "" });
                      }}
                      className="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 font-semibold transition-colors"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-md p-8 text-center">
                <p className="text-gray-500 text-lg">Select a product to review</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </Container>
  );
}
