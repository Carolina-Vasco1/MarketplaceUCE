import { http, getUserEmail } from "./http";

export type BuyPayload = {
  product_id: string;
  amount: number;
};

export type BuyResponse = {
  order_id: string;
  approval_url?: string;
  status?: string;
};

const BASE = "/order/api/v1/orders";

export async function createOrderAndPay(payload: BuyPayload) {
  const email = getUserEmail(); // el interceptor también manda X-User-Email

  const r = await http.post<BuyResponse>(`${BASE}/buy`, {
    buyer_id: email || undefined,
    product_id: payload.product_id,
    amount: payload.amount,
  });

  return r.data;
}

export const ordersAPI = {
  async createOrder(data: any) {
    const r = await http.post(`${BASE}`, data);
    return r.data;
  },

  async getMyOrders(filter?: any) {
    const r = await http.get(`${BASE}/me`, { params: filter });
    return r.data;
  },

  async getOrder(orderId: string) {
    const r = await http.get(`${BASE}/${orderId}`);
    return r.data;
  },

  async createFromCart(payload: any) {
    const r = await http.post(`${BASE}/create-from-cart`, payload);
    return r.data;
  },
};
