import { useState, useEffect } from "react";
import Container from "../components/Container";
import { reportingAPI } from "../api/reporting";

export default function AnalyticsPage() {
  const [metrics, setMetrics] = useState<any>(null);
  const [salesReport, setSalesReport] = useState<any>(null);
  const [period, setPeriod] = useState("week");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, [period]);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const [sales, metrics_data] = await Promise.all([
        reportingAPI.getSellerSalesReports(period),
        reportingAPI.getSellerSalesMetrics(period),
      ]);
      setSalesReport(sales);
      setMetrics(metrics_data);
    } catch (error) {
      console.error("Failed to load analytics:", error);
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
        <h1 className="text-4xl font-bold text-gray-900 mb-8">📊 Sales Analytics</h1>

        {/* Period Selector */}
        <div className="flex gap-2 mb-8">
          {["day", "week", "month", "year"].map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                period === p
                  ? "bg-primary-500 text-white"
                  : "bg-gray-200 text-gray-700 hover:bg-gray-300"
              }`}
            >
              {p.charAt(0).toUpperCase() + p.slice(1)}
            </button>
          ))}
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="bg-gradient-to-br from-primary-500 to-primary-600 text-white rounded-lg p-6 shadow-md">
            <p className="text-sm opacity-90">Total Sales</p>
            <p className="text-3xl font-bold mt-2">
              ${metrics?.total_sales?.toFixed(2) || "0.00"}
            </p>
            <p className="text-sm mt-2 opacity-75">
              {metrics?.sales_growth}% vs last period
            </p>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-green-600 text-white rounded-lg p-6 shadow-md">
            <p className="text-sm opacity-90">Total Orders</p>
            <p className="text-3xl font-bold mt-2">
              {metrics?.total_orders || 0}
            </p>
            <p className="text-sm mt-2 opacity-75">
              {metrics?.avg_order_value && `Avg: $${metrics.avg_order_value.toFixed(2)}`}
            </p>
          </div>

          <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-lg p-6 shadow-md">
            <p className="text-sm opacity-90">Active Products</p>
            <p className="text-3xl font-bold mt-2">
              {metrics?.active_products || 0}
            </p>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-purple-600 text-white rounded-lg p-6 shadow-md">
            <p className="text-sm opacity-90">Conversion Rate</p>
            <p className="text-3xl font-bold mt-2">
              {metrics?.conversion_rate?.toFixed(1) || "0"}%
            </p>
          </div>
        </div>

        {/* Charts Area */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Sales Trend */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Sales Trend</h2>
            <div className="h-64 bg-gradient-to-b from-primary-50 to-transparent rounded-lg flex items-end justify-center gap-1 p-4">
              {salesReport?.daily_sales?.map((sale: any, i: number) => (
                <div
                  key={i}
                  className="flex-1 bg-primary-500 rounded-t-lg hover:bg-primary-600 transition-colors"
                  style={{ height: `${(sale.amount / 1000) * 100}%` }}
                  title={`${sale.date}: $${sale.amount}`}
                />
              ))}
            </div>
            <p className="text-sm text-gray-600 text-center mt-4">
              Daily sales over {period}
            </p>
          </div>

          {/* Top Products */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Top Products</h2>
            <div className="space-y-3">
              {metrics?.top_products?.map((product: any, i: number) => (
                <div key={i} className="flex justify-between items-center pb-3 border-b last:border-b-0">
                  <div>
                    <p className="font-semibold text-gray-900">{product.name}</p>
                    <p className="text-sm text-gray-600">{product.quantity} sold</p>
                  </div>
                  <p className="font-bold text-primary-600">${product.revenue.toFixed(2)}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Sales Details Table */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Sales Details</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-4 py-2 text-left font-semibold">Date</th>
                  <th className="px-4 py-2 text-left font-semibold">Orders</th>
                  <th className="px-4 py-2 text-left font-semibold">Revenue</th>
                  <th className="px-4 py-2 text-left font-semibold">Avg Order Value</th>
                </tr>
              </thead>
              <tbody>
                {salesReport?.daily_sales?.map((sale: any, i: number) => (
                  <tr key={i} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-2">{sale.date}</td>
                    <td className="px-4 py-2">{sale.orders}</td>
                    <td className="px-4 py-2 font-semibold text-green-600">
                      ${sale.amount.toFixed(2)}
                    </td>
                    <td className="px-4 py-2">${(sale.amount / sale.orders).toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Container>
  );
}
