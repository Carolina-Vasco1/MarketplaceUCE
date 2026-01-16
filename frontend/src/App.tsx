import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Marketplace from "./pages/Marketplace";
import ProductDetail from "./pages/ProductDetail";
import Login from "./pages/Login";
import RegisterOTP from "./pages/RegisterOTP";
import SellProduct from "./pages/SellProduct";
import MyProducts from "./pages/MyProducts";
import CartPage from "./pages/CartPage";

import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminUsers from "./pages/admin/AdminUsers";
import AdminProducts from "./pages/admin/AdminProducts";
import AdminReportsPage from "./pages/AdminReportsPage";

// Nueva páginas de servicios
import SearchPage from "./pages/SearchPage";
import ReviewsPage from "./pages/ReviewsPage";
import UserProfilePage from "./pages/UserProfilePage";
import RecommendationsPage from "./pages/RecommendationsPage";
import OrdersPage from "./pages/OrdersPage";
import AnalyticsPage from "./pages/AnalyticsPage";

import { Guard } from "./auth/guard";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        {/* Marketplace */}
        <Route path="/" element={<Marketplace />} />
        <Route path="/products/:id" element={<ProductDetail />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/cart" element={<CartPage />} />

        {/* Auth */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<RegisterOTP />} />

        {/* User */}
        <Route
          path="/profile"
          element={
            <Guard roles={["user", "seller", "admin"]}>
              <UserProfilePage />
            </Guard>
          }
        />
        <Route
          path="/reviews"
          element={
            <Guard roles={["user", "seller", "admin"]}>
              <ReviewsPage />
            </Guard>
          }
        />
        <Route
          path="/recommendations"
          element={<RecommendationsPage />}
        />

        {/* Seller */}
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
          path="/my-orders"
          element={
            <Guard roles={["user", "seller", "admin"]}>
              <OrdersPage />
            </Guard>
          }
        />
        <Route
          path="/analytics"
          element={
            <Guard roles={["seller", "admin"]}>
              <AnalyticsPage />
            </Guard>
          }
        />

        {/* Admin */}
        <Route
          path="/admin"
          element={
            <Guard roles={["admin"]}>
              <AdminDashboard />
            </Guard>
          }
        />
        <Route
          path="/admin/dashboard"
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
        <Route
          path="/admin/reports"
          element={
            <Guard roles={["admin"]}>
              <AdminReportsPage />
            </Guard>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
