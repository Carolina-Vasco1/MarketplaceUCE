import { http } from "./http";
import type { Product, ProductCreate } from "../types/models";

export async function listProducts() {
  const r = await http.get<Product[]>("/products/");
  return r.data;
}

export async function listMyProducts(seller_id: string) {
  const r = await http.get<Product[]>("/products/", { params: { seller_id } });
  return r.data;
}

export async function getProduct(id: string) {
  const r = await http.get<Product>(`/products/${id}`);
  return r.data;
}

export async function createProduct(payload: ProductCreate) {
  const r = await http.post<Product>("/products/", payload);
  return r.data;
}

export async function deleteProduct(id: string) {
  const r = await http.delete(`/products/${id}`);
  return r.data;
}

export async function uploadProductImage(file: File) {
  const form = new FormData();
  form.append("file", file);

  const r = await http.post<{ url: string }>("/products/upload/image", form);
  return r.data.url;
}

// ✅ UPDATE REAL (tu backend lo soporta ahora)
export async function updateProduct(
  id: string,
  payload: Partial<Pick<Product, "title" | "description" | "price" | "category_id" | "images">>
) {
  const r = await http.patch<Product>(`/products/${id}`, payload);
  return r.data;
}
