import { http } from "./http";

const SEARCH_SERVICE_URL = "/products/api/v1";

export const searchAPI = {
  searchProducts: (q: string, filters: any = {}) =>
    http.get(`${SEARCH_SERVICE_URL}/products`, {
      params: { q, ...filters },
    }),

  getSuggestions: (q: string, limit = 10) =>
    http.get(`${SEARCH_SERVICE_URL}/products`, {
      params: { q, limit },
    }),

  rebuildIndex: () =>
    http.post(`${SEARCH_SERVICE_URL}/search/index/rebuild`),
};
