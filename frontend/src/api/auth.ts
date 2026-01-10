import { http } from "./http";

export async function requestOtp(email: string) {
  const r = await http.post("/auth/request-otp", { email });
  return r.data;
}

export async function verifyOtp(email: string, code: string) {
  const r = await http.post("/auth/verify-otp", { email, code });
  return r.data;
}

export async function register(email: string, password: string, role: string) {
  const r = await http.post("/auth/register", { email, password, role });
  return r.data; // {access_token}
}

export async function login(email: string, password: string) {
  const r = await http.post("/auth/login", { email, password });
  return r.data; // {access_token}
}
