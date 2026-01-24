import { http } from "./http";

const ADMIN_SERVICE_URL = "/admin/api/v1";

export const reportingAdminAPI = {
  // Dashboard
  getDashboard: () =>
    http.get(`${ADMIN_SERVICE_URL}/admin/dashboard`),

  getSettings: () =>
    http.get(`${ADMIN_SERVICE_URL}/admin/settings`),

  updateSettings: (data: any) =>
    http.put(`${ADMIN_SERVICE_URL}/admin/settings`, data),

  // Users
  createAdminUser: (data: any) =>
    http.post(`${ADMIN_SERVICE_URL}/admin/users`, data),

  listAdminUsers: (skip = 0, limit = 10) =>
    http.get(`${ADMIN_SERVICE_URL}/admin/users`, {
      params: { skip, limit },
    }),

  getAdminUser: (userId: string) =>
    http.get(`${ADMIN_SERVICE_URL}/admin/users/${userId}`),

  deleteAdminUser: (userId: string) =>
    http.delete(`${ADMIN_SERVICE_URL}/admin/users/${userId}`),

  // Reports
  createReport: (data: any) =>
    http.post(`${ADMIN_SERVICE_URL}/admin/reports`, data),

  listReports: (status?: string, skip = 0, limit = 20) =>
    http.get(`${ADMIN_SERVICE_URL}/admin/reports`, {
      params: { status, skip, limit },
    }),

  getReport: (reportId: string) =>
    http.get(`${ADMIN_SERVICE_URL}/admin/reports/${reportId}`),

  updateReportStatus: (reportId: string, status: string) =>
    http.put(`${ADMIN_SERVICE_URL}/admin/reports/${reportId}`, {
      status,
    }),
};

// Backward compatibility
export const adminAPI = reportingAdminAPI;
