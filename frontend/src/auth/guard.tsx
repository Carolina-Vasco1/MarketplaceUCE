import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import { getToken } from "./token";
import type { Role } from "../types/models";

type Props = { children: React.ReactNode; roles?: Role[] };

export function Guard({ children, roles }: Props) {
  const token = getToken();
  const loc = useLocation();

  if (!token) return <Navigate to="/login" replace state={{ from: loc.pathname }} />;

  try {
    const payload: any = jwtDecode(token);
    const role: Role | undefined = payload?.role;

    if (roles && role && !roles.includes(role)) return <Navigate to="/" replace />;
    return <>{children}</>;
  } catch {
    return <Navigate to="/login" replace />;
  }
}
