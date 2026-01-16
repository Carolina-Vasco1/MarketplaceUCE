import { http } from "./http";

const REVIEW_SERVICE_URL = "/review/api/v1";

export const reviewsAPI = {
  createReview: (data: any) =>
    http.post(`${REVIEW_SERVICE_URL}/reviews`, data),

  getProductReviews: (productId: string, skip = 0, limit = 20) =>
    http.get(`${REVIEW_SERVICE_URL}/reviews/product/${productId}?skip=${skip}&limit=${limit}`),

  getProductStats: (productId: string) =>
    http.get(`${REVIEW_SERVICE_URL}/reviews/product/${productId}/stats`),

  getReviewById: (id: string) =>
    http.get(`${REVIEW_SERVICE_URL}/reviews/${id}`),

  updateReview: (id: string, data: any) =>
    http.put(`${REVIEW_SERVICE_URL}/reviews/${id}`, data),

  deleteReview: (id: string) =>
    http.delete(`${REVIEW_SERVICE_URL}/reviews/${id}`),

  // Get products available for review
  getProductsForReview: () =>
    http.get(`${REVIEW_SERVICE_URL}/reviews/my-products`),

  // Get user's reviews
  getUserReviews: (userId?: string) =>
    http.get(`${REVIEW_SERVICE_URL}/reviews/user/${userId || 'me'}`),

  // Get average rating for product
  getAverageRating: (productId: string) =>
    http.get(`${REVIEW_SERVICE_URL}/reviews/product/${productId}/rating`),
};

// Export the old name for backward compatibility
export const reviewAPI = reviewsAPI;
