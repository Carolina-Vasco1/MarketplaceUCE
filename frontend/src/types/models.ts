export type Role = "buyer" | "seller" | "admin" | "user";

export type Product = {
  id: string;
  title: string;
  description: string;
  price: number;
  original_price?: number;
  category?: string;
  category_id?: string;
  seller_id: string;
  seller_name?: string;
  images?: string[];
  image_url?: string;
  rating?: number;
  review_count?: number;
  stock?: number;
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
  is_active: boolean;
  created_at?: string;

  is_verified?: boolean;
};
