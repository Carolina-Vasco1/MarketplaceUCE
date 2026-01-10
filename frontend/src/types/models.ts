export type Role = "buyer" | "seller" | "admin";

export type Product = {
  id: string;
  title: string;
  description: string;
  price: number;
  category_id?: string;
  seller_id: string;
  images?: string[];
  created_at?: string;
};

export type ProductCreate = {
  title: string;
  description: string;
  price: number;
  category_id?: string;
  seller_id: string;
  images?: string[];
};

export type AdminUser = {
  id: string;
  email: string;
  role: Role;
  is_verified: boolean;
  is_active: boolean;
  created_at?: string;
};
