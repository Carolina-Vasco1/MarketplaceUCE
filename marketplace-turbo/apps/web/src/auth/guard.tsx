import React, { useEffect } from "react";
import { Navigate, useLocation } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import { getToken } from "./token";
import type { Role } from "../types/models";
import { useCart } from "../store/cartStore"; // ✅ ajusta la ruta si tu archivo se llama distinto

type Props = { children: React.ReactNode; roles?: Role[] };

export function Guard({ children, roles }: Props) {
  const token = getToken();
  const loc = useLocation();

  useEffect(() => {
    if (!token) {
      useCart.getState().setUser(undefined);
      return;
    }

    try {
      const payload: any = jwtDecode(token);
      const uid = payload?.sub ? String(payload.sub) : undefined;
      useCart.getState().setUser(uid);
    } catch {
      useCart.getState().setUser(undefined);
    }
  }, [token]);

  if (!token) return <Navigate to="/login" replace state={{ from: loc.pathname }} />;

  try {
    const payload: any = jwtDecode(token);
    let role: Role | undefined = payload?.role;

    // Map 'buyer' to 'user' for consistency
    if (role === "buyer") {
      role = "user" as Role;
    }

    if (roles && role && !roles.includes(role)) return <Navigate to="/" replace />;
    return <>{children}</>;
  } catch {
    return <Navigate to="/login" replace />;
  }
}

