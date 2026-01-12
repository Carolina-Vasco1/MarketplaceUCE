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
  const r = await http.post<BuyResponse>("/orders/buy", payload);
  return r.data;
}
