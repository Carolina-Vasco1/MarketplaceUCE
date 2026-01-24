import { useEffect } from "react";
import { useCart } from "../store/cartStore";
import { getSession } from "../auth/session";

export default function CartBootstrapper() {
  const { setUser } = useCart();

  useEffect(() => {
    const s = getSession();
    setUser(s?.user_id); // si no hay sesión => guest

    const onLogout = () => setUser(undefined);
    window.addEventListener("logout", onLogout);
    return () => window.removeEventListener("logout", onLogout);
  }, [setUser]);

  return null;
}
