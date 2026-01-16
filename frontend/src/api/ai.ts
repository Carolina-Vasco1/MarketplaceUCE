import { http } from "./http";

const AI_SERVICE_URL = "/ai/api/v1";

export const aiAPI = {
  // Recommendations
  getRecommendations: (userId: string, limit = 10, category?: string) =>
    http.post(`${AI_SERVICE_URL}/recommendations/for-user`, {
      user_id: userId,
      limit,
      category,
    }),

  getSimilarProducts: (productId: string, limit = 5) =>
    http.post(`${AI_SERVICE_URL}/recommendations/similar-products`, {
      product_id: productId,
      limit,
    }),

  getTrendingProducts: (limit = 10, category?: string) =>
    http.post(`${AI_SERVICE_URL}/recommendations/trending`, {
      limit,
      category,
    }),

  // NLP
  analyzeSentiment: (text: string) =>
    http.post(`${AI_SERVICE_URL}/nlp/sentiment`, { text }),

  classifyText: (text: string) =>
    http.post(`${AI_SERVICE_URL}/nlp/classify`, { text }),

  extractKeywords: (text: string) =>
    http.post(`${AI_SERVICE_URL}/nlp/extract-keywords`, { text }),

  // Image Analysis
  analyzeImageQuality: (imageUrl: string) =>
    http.post(`${AI_SERVICE_URL}/images/analyze-quality`, {
      image_url: imageUrl,
    }),

  detectObjects: (imageUrl: string) =>
    http.post(`${AI_SERVICE_URL}/images/detect-objects`, {
      image_url: imageUrl,
    }),

  validateProductImage: (imageUrl: string) =>
    http.post(`${AI_SERVICE_URL}/images/validate-product-image`, {
      image_url: imageUrl,
    }),
};
