import { Link } from "react-router-dom";
import { useCart } from "../store/cartStore";
import type { Product } from "../types/models";

interface ProductCardProps {
  product?: Product;
  p?: Product;
}

export default function ProductCard({ product, p }: ProductCardProps) {
  const prod = product || p;
  const { addItem } = useCart();
  if (!prod) return null;

  const img = prod.images?.[0];
  const rating = prod.rating || 4.5;
  const reviewCount = prod.review_count || Math.floor(Math.random() * 100);
  const inStock = (prod.stock ?? 1) > 0;

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    addItem({
      id: prod.id,
      title: prod.title,
      price: prod.price,
      quantity: 1,
      image_url: img ? `http://localhost:8000${img}` : undefined,
    });
    alert("Product added to cart!");
  };

  return (
    <Link to={`/products/${prod.id}`}>
      <div className="bg-white rounded-lg shadow-sm hover:shadow-lg hover:scale-105 transition-all duration-300 overflow-hidden flex flex-col h-full group">
        {/* Image Container */}
        <div className="relative h-48 bg-gray-100 overflow-hidden">
          {img ? (
            <img
              src={`http://localhost:8000${img}`}
              className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
              alt={prod.title}
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-400">
              📦
            </div>
          )}

          {/* Stock Badge */}
          {!inStock && (
            <div className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded-full text-xs font-semibold">
              Out of Stock
            </div>
          )}
          {inStock && (prod.stock ?? 1) < 10 && (
            <div className="absolute top-2 right-2 bg-orange-500 text-white px-2 py-1 rounded-full text-xs font-semibold">
              Only {prod.stock} left
            </div>
          )}
        </div>

        {/* Content */}
        <div className="p-4 flex flex-col flex-grow">
          {/* Title */}
          <h3 className="font-semibold text-gray-900 line-clamp-2 mb-2 group-hover:text-primary-600 transition-colors">
            {prod.title}
          </h3>

          {/* Description */}
          <p className="text-sm text-gray-600 line-clamp-2 mb-3">
            {prod.description}
          </p>

          {/* Rating */}
          <div className="flex items-center gap-2 mb-3">
            <div className="flex text-yellow-400 text-sm">
              {"⭐".repeat(Math.floor(rating))}
            </div>
            <span className="text-sm text-gray-600">
              ({reviewCount})
            </span>
          </div>

          {/* Price */}
          <div className="flex items-center justify-between mb-4 mt-auto">
            <div className="flex items-baseline gap-2">
              <span className="text-2xl font-bold text-primary-600">
                ${prod.price.toFixed(2)}
              </span>
              {prod.original_price && (
                <span className="text-sm text-gray-500 line-through">
                  ${prod.original_price.toFixed(2)}
                </span>
              )}
            </div>
            {prod.original_price && (
              <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded-full font-semibold">
                {Math.round(
                  ((prod.original_price - prod.price) / prod.original_price) * 100
                )}
                % OFF
              </span>
            )}
          </div>

          {/* Seller Info */}
          <p className="text-xs text-gray-500 mb-4">
            by {prod.seller_name || "Unknown Seller"}
          </p>

          {/* Buttons */}
          <div className="grid grid-cols-2 gap-2">
            <Link to={`/products/${prod.id}`} className="col-span-1">
              <button className="w-full bg-primary-500 hover:bg-primary-600 text-white font-semibold py-2 rounded-lg transition-colors">
                Details
              </button>
            </Link>
            <button
              onClick={handleAddToCart}
              disabled={!inStock}
              className="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-2 rounded-lg transition-colors disabled:opacity-50"
            >
              {inStock ? "🛒 Add to Cart" : "Out"}
            </button>
          </div>
        </div>
      </div>
    </Link>
  );
}
