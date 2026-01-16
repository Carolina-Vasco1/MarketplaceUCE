import { http } from "./http";

const REPORTING_SERVICE_URL = "/reporting/api/v1";

export const reportingAPI = {
  // Sales Reports
  getSellerSalesReports: (sellerId: string, period = "monthly", months = 12) =>
    http.get(`${REPORTING_SERVICE_URL}/reports/sales/${sellerId}`, {
      params: { period, months },
    }),

  getSellerSalesSummary: (sellerId: string) =>
    http.get(`${REPORTING_SERVICE_URL}/reports/sales/${sellerId}/summary`),

  // Sales Metrics
  getSellerSalesMetrics: (sellerId: string, startDate?: string, endDate?: string) =>
    http.get(`${REPORTING_SERVICE_URL}/sales/by-seller/${sellerId}`, {
      params: { start_date: startDate, end_date: endDate },
    }),

  getProductSales: (productId: string) =>
    http.get(`${REPORTING_SERVICE_URL}/sales/by-product/${productId}`),

  getPlatformSalesSummary: () =>
    http.get(`${REPORTING_SERVICE_URL}/sales/platform/summary`),

  // Analytics
  getDashboardAnalytics: (period = "monthly") =>
    http.get(`${REPORTING_SERVICE_URL}/analytics/dashboard`, {
      params: { period },
    }),

  getUserGrowth: (period = "monthly") =>
    http.get(`${REPORTING_SERVICE_URL}/analytics/user-growth`, {
      params: { period },
    }),

  getTrafficMetrics: (period = "daily") =>
    http.get(`${REPORTING_SERVICE_URL}/analytics/traffic`, {
      params: { period },
    }),

  getConversionMetrics: (period = "monthly") =>
    http.get(`${REPORTING_SERVICE_URL}/analytics/conversion`, {
      params: { period },
    }),
};
