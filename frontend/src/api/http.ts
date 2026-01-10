import axios from "axios";
import { getToken } from "../auth/token";

export const http = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 15000,
});

http.interceptors.request.use((config) => {
  const token = getToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
