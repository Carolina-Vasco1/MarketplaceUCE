import { useState, useEffect } from "react";
import Container from "../components/Container";
import { reportingAdminAPI } from "../api/reporting_admin";

export default function AdminReportsPage() {
  const [dashboard, setDashboard] = useState<any>(null);
  const [reports, setReports] = useState<any[]>([]);
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [dash, reps] = await Promise.all([
        reportingAdminAPI.getDashboard(),
        reportingAdminAPI.listReports(),
      ]);
      setDashboard(dash);
      setReports((reps as any)?.reports || reps?.data || reps);
    } catch (error) {
      console.error("Failed to load admin data:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Container>
        <div className="py-12 text-center">
          <div className="inline-block animate-spin text-primary-500 text-4xl">⏳</div>
        </div>
      </Container>
    );
  }

  return (
    <Container>
      <div className="py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">📊 Admin Reports</h1>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-lg p-6 shadow-md">
            <p className="text-sm opacity-90">Total Users</p>
            <p className="text-3xl font-bold mt-2">
              {dashboard?.total_users || 0}
            </p>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-green-600 text-white rounded-lg p-6 shadow-md">
            <p className="text-sm opacity-90">Total Products</p>
            <p className="text-3xl font-bold mt-2">
              {dashboard?.total_products || 0}
            </p>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-purple-600 text-white rounded-lg p-6 shadow-md">
            <p className="text-sm opacity-90">Total Revenue</p>
            <p className="text-3xl font-bold mt-2">
              ${dashboard?.total_revenue?.toFixed(2) || "0.00"}
            </p>
          </div>

          <div className="bg-gradient-to-br from-orange-500 to-orange-600 text-white rounded-lg p-6 shadow-md">
            <p className="text-sm opacity-90">Total Orders</p>
            <p className="text-3xl font-bold mt-2">
              {dashboard?.total_orders || 0}
            </p>
          </div>
        </div>

        {/* System Statistics */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">System Statistics</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="text-gray-600 text-sm mb-2">Active Sellers</p>
              <p className="text-2xl font-bold text-primary-600">
                {dashboard?.active_sellers || 0}
              </p>
            </div>
            <div>
              <p className="text-gray-600 text-sm mb-2">Active Buyers</p>
              <p className="text-2xl font-bold text-primary-600">
                {dashboard?.active_buyers || 0}
              </p>
            </div>
            <div>
              <p className="text-gray-600 text-sm mb-2">Average Order Value</p>
              <p className="text-2xl font-bold text-primary-600">
                ${dashboard?.avg_order_value?.toFixed(2) || "0.00"}
              </p>
            </div>
          </div>
        </div>

        {/* Reports List */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Generated Reports</h2>
            <button className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors">
              + Generate Report
            </button>
          </div>

          {/* Filter */}
          <div className="flex gap-2 mb-6">
            {["all", "pending", "completed", "failed"].map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                  filter === f
                    ? "bg-primary-500 text-white"
                    : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                }`}
              >
                {f.charAt(0).toUpperCase() + f.slice(1)}
              </button>
            ))}
          </div>

          {/* Reports Table */}
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-4 py-2 text-left font-semibold">Report Name</th>
                  <th className="px-4 py-2 text-left font-semibold">Type</th>
                  <th className="px-4 py-2 text-left font-semibold">Status</th>
                  <th className="px-4 py-2 text-left font-semibold">Created</th>
                  <th className="px-4 py-2 text-left font-semibold">Action</th>
                </tr>
              </thead>
              <tbody>
                {reports.map((report) => (
                  <tr key={report.id} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-2 font-semibold text-gray-900">
                      {report.name}
                    </td>
                    <td className="px-4 py-2 text-gray-600">
                      {report.type}
                    </td>
                    <td className="px-4 py-2">
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-semibold ${
                          report.status === "completed"
                            ? "bg-green-100 text-green-700"
                            : report.status === "pending"
                            ? "bg-yellow-100 text-yellow-700"
                            : "bg-red-100 text-red-700"
                        }`}
                      >
                        {report.status}
                      </span>
                    </td>
                    <td className="px-4 py-2 text-gray-600">
                      {new Date(report.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-4 py-2">
                      {report.status === "completed" && (
                        <button className="text-primary-600 hover:text-primary-700 font-semibold">
                          Download
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {reports.length === 0 && (
            <div className="text-center py-8">
              <p className="text-gray-500">No reports available</p>
            </div>
          )}
        </div>
      </div>
    </Container>
  );
}
