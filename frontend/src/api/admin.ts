import { http } from "./http";
import type { AdminUser, Product } from "../types/models";

export async function adminListUsers() {
  const r = await http.get<AdminUser[]>("/api/v1/admin/users");
  return r.data;
}

export async function adminSetUserRole(user_id: string, role: "buyer" | "seller" | "admin") {
  const r = await http.patch(`/api/v1/admin/users/${user_id}/role`, { role });
  return r.data;
}

export async function adminSetUserActive(user_id: string, is_active: boolean) {
  const r = await http.patch(`/api/v1/admin/users/${user_id}/active`, { is_active });
  return r.data;
}

export async function adminListProducts() {
  const r = await http.get<Product[]>("/api/v1/admin/products");
  return r.data;
}

export async function adminDeleteProduct(product_id: string) {
  const r = await http.delete(`/api/v1/admin/products/${product_id}`);
  return r.data;
}
