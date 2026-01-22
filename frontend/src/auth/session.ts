import { jwtDecode } from "jwt-decode";
import { getToken } from "./token";
import type { Role } from "../types/models";

export function getSession() {
  const token = getToken();
  if (!token) return null;

  try {
    const p: any = jwtDecode(token);
    const user_id = p?.sub ? String(p.sub) : undefined;

    return {
      token,
      user_id: user_id ?? "",
      role: (p?.role as Role) || "buyer",
    };
  } catch {
    return null;
  }
}

