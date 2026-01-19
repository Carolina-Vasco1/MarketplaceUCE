import { http } from "./http";

export type BuyPayload = {
  product_id: string;
  amount: number;
};

export type BuyResponse = {
  order_id: string;
  approval_url?: string;
  status?: string;
};

export async function createOrderAndPay(payload: BuyPayload) {
  const r = await http.post<BuyResponse>("/order/api/v1/orders/buy", payload);
  return r.data;
}

const API_URL = "/order/api/v1/orders";

export const ordersAPI = {
  // Create an order
  async createOrder(data: any) {
    const response = await http.post(`${API_URL}`, data);
    return response.data;
  },

  // Get my orders
  async getMyOrders(filter?: any) {
    const response = await http.get(`${API_URL}/me`, { params: filter });
    return response.data;
  },

  // Get order by ID
  async getOrder(orderId: string) {
    const response = await http.get(`${API_URL}/${orderId}`);
    return response.data;
  },

  // Update order status
  async updateOrderStatus(orderId: string, status: string) {
    const response = await http.put(`${API_URL}/${orderId}/status`, { status });
    return response.data;
  },

  // Cancel order
  async cancelOrder(orderId: string) {
    const response = await http.post(`${API_URL}/${orderId}/cancel`);
    return response.data;
  },

  // Get order history
  async getOrderHistory(limit: number = 50) {
    const response = await http.get(`${API_URL}/history`, {
      params: { limit },
    });
    return response.data;
  },

  // Track order
  async trackOrder(orderId: string) {
    const response = await http.get(`${API_URL}/${orderId}/track`);
    return response.data;
  },
};
