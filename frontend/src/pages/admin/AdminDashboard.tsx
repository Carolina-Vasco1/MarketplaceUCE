import Container from "../../components/Container";
import AdminSidebar from "../../components/AdminSidebar";

export default function AdminDashboard() {
  return (
    <Container>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="md:col-span-1">
          <AdminSidebar />
        </div>

        <div className="md:col-span-3">
          <h1 className="text-2xl font-semibold mb-3">Admin Dashboard</h1>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="border rounded-xl p-4 bg-white">Users</div>
            <div className="border rounded-xl p-4 bg-white">Products</div>
            <div className="border rounded-xl p-4 bg-white">Orders</div>
          </div>

          <p className="text-sm text-gray-600 mt-4">
            Note: Admin endpoints must exist in the Gateway (e.g., /admin/users).
          </p>
        </div>
      </div>
    </Container>
  );
}
