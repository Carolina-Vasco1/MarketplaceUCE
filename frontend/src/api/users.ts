import { http } from "./http";

const USER_SERVICE_URL = "/user/api/v1";

export const userAPI = {
  getProfile: (userId: string) =>
    http.get(`${USER_SERVICE_URL}/users/${userId}`),

  updateProfile: (userId: string, data: any) =>
    http.put(`${USER_SERVICE_URL}/users/${userId}`, data),

  listUsers: (skip = 0, limit = 10) =>
    http.get(`${USER_SERVICE_URL}/users?skip=${skip}&limit=${limit}`),

  getUserByEmail: (email: string) =>
    http.get(`${USER_SERVICE_URL}/users?email=${email}`),
};
