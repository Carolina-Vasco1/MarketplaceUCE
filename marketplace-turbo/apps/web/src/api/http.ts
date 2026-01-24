import axios from "axios";
import { getToken } from "../auth/token";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export function getUserEmail(): string {
  const direct =
    localStorage.getItem("userEmail") ||
    localStorage.getItem("email") ||
    "";

  if (direct) return direct.trim().toLowerCase();

  const userRaw = localStorage.getItem("user");
  if (!userRaw) return "";

  try {
    const u = JSON.parse(userRaw);
    return String(u?.email ?? "").trim().toLowerCase();
  } catch {
    return "";
  }
}

export const http = axios.create({
  baseURL: API_URL,
  timeout: 15000,
});

http.interceptors.request.use((config) => {
  const token = getToken();
  const email = getUserEmail();

  config.headers = config.headers ?? {};

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  if (email) {
    config.headers["X-User-Email"] = email;
  }

  return config;
});
