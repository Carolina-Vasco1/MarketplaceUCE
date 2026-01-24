import { http } from "./http";

const CATEGORY_SERVICE_URL = "/category/api/v1";

export const categoryAPI = {
  getCategories: (skip = 0, limit = 50) =>
    http.get(`${CATEGORY_SERVICE_URL}/categories?skip=${skip}&limit=${limit}`),

  getCategoryTree: () =>
    http.get(`${CATEGORY_SERVICE_URL}/categories/tree`),

  getCategoryById: (id: string) =>
    http.get(`${CATEGORY_SERVICE_URL}/categories/${id}`),

  createCategory: (data: any) =>
    http.post(`${CATEGORY_SERVICE_URL}/categories`, data),

  updateCategory: (id: string, data: any) =>
    http.put(`${CATEGORY_SERVICE_URL}/categories/${id}`, data),

  deleteCategory: (id: string) =>
    http.delete(`${CATEGORY_SERVICE_URL}/categories/${id}`),
};
