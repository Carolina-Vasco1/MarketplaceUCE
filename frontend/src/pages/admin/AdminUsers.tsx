import { useEffect, useState } from "react";
import Container from "../../components/Container";
import AdminSidebar from "../../components/AdminSidebar";
import type { AdminUser, Role } from "../../types/models";
import {
  adminListUsers,
  adminSetUserActive,
  adminSetUserRole,
} from "../../api/admin";

export default function AdminUsers() {
  const [items, setItems] = useState<AdminUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

  async function load() {
    setErr("");
    setLoading(true);
    try {
      setItems(await adminListUsers());
    } catch (e: any) {
      setErr(
        e?.response?.data?.detail ??
          "Unable to load users (missing admin endpoint)."
      );
    } finally {
      setLoading(false);
    }
  }

  async function changeRole(u: AdminUser, role: Role) {
    try {
      if (role !== "user") {
        await adminSetUserRole(u.id, role as "buyer" | "seller" | "admin");
        await load();
      }
    } catch (e: any) {
      alert(e?.response?.data?.detail ?? "Unable to change role.");
    }
  }

  async function toggleActive(u: AdminUser) {
    try {
      await adminSetUserActive(u.id, !u.is_active);
      await load();
    } catch (e: any) {
      alert(e?.response?.data?.detail ?? "Unable to update user.");
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <Container>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="md:col-span-1">
          <AdminSidebar />
        </div>

        <div className="md:col-span-3">
          <h1 className="text-2xl font-semibold mb-3">Users</h1>

          {loading && <p>Loading...</p>}
          {err && <p className="text-red-700 text-sm">{err}</p>}

          {!loading && !err && (
            <div className="space-y-3">
              {items.map((u) => (
                <div key={u.id} className="border rounded-xl p-4 bg-white">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                    <div>
                      <div className="font-semibold">{u.email}</div>
                      <div className="text-xs text-gray-500">
                        id: {u.id} | active: {String(u.is_active)}
                      </div>
                    </div>

                    <div className="flex flex-wrap gap-2">
                      <select
                        className="border rounded-lg px-2 py-1 text-sm"
                        value={u.role}
                        onChange={(e) =>
                          changeRole(u, e.target.value as Role)
                        }
                      >
                        <option value="buyer">buyer</option>
                        <option value="seller">seller</option>
                        <option value="admin">admin</option>
                      </select>

                      <button
                        className="border rounded-lg px-3 py-1 text-sm"
                        onClick={() => toggleActive(u)}
                      >
                        {u.is_active ? "Deactivate" : "Activate"}
                      </button>
                    </div>
                  </div>
                </div>
              ))}

              {items.length === 0 && (
                <div className="text-gray-600">No users found.</div>
              )}
            </div>
          )}
        </div>
      </div>
    </Container>
  );
}
