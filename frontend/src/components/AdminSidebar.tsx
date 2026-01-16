import { Link } from "react-router-dom";

export default function AdminSidebar() {
  return (
    <div className="w-64 bg-gray-100 border-r border-gray-300 p-4">
      <h2 className="font-bold text-lg mb-4">Admin Menu</h2>
      <nav className="space-y-2">
        <Link to="/admin/dashboard" className="block px-4 py-2 rounded hover:bg-gray-200">
          Dashboard
        </Link>
        <Link to="/admin/products" className="block px-4 py-2 rounded hover:bg-gray-200">
          Products
        </Link>
        <Link to="/admin/users" className="block px-4 py-2 rounded hover:bg-gray-200">
          Users
        </Link>
      </nav>
    </div>
  );
}
