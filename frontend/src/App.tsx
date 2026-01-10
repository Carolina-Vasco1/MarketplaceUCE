import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Marketplace from "./pages/Marketplace";
import ProductDetail from "./pages/ProductDetail";
import Login from "./pages/Login";
import RegisterOTP from "./pages/RegisterOTP";
import SellProduct from "./pages/SellProduct";
import MyProducts from "./pages/MyProducts";

import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminUsers from "./pages/admin/AdminUsers";
import AdminProducts from "./pages/admin/AdminProducts";

import { Guard } from "./auth/guard";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Marketplace />} />
        <Route path="/products/:id" element={<ProductDetail />} />

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<RegisterOTP />} />

        <Route
          path="/sell"
          element={
            <Guard roles={["seller", "admin"]}>
              <SellProduct />
            </Guard>
          }
        />
        <Route
          path="/my-products"
          element={
            <Guard roles={["seller", "admin"]}>
              <MyProducts />
            </Guard>
          }
        />

        <Route
          path="/admin"
          element={
            <Guard roles={["admin"]}>
              <AdminDashboard />
            </Guard>
          }
        />
        <Route
          path="/admin/users"
          element={
            <Guard roles={["admin"]}>
              <AdminUsers />
            </Guard>
          }
        />
        <Route
          path="/admin/products"
          element={
            <Guard roles={["admin"]}>
              <AdminProducts />
            </Guard>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
