import { apiGet, apiPost, apiPostForm, apiPut } from "./apiClient";
import type {
  AdminLoginResponse,
  AdminLogoutResponse,
  AdminPasswordChangeResponse,
  AdminSettingsResponse,
  AdminSettingsUpdate,
  AdminStatusResponse
} from "../types/admin";
import type { Floor } from "../types/survey";

function authHeaders(token: string): HeadersInit {
  return {
    Authorization: `Bearer ${token}`
  };
}

export async function getAdminStatus(): Promise<AdminStatusResponse> {
  return apiGet<AdminStatusResponse>("/admin/status");
}

export async function setupAdminPassword(password: string): Promise<AdminStatusResponse> {
  return apiPost<AdminStatusResponse>("/admin/setup", { password });
}

export async function loginAdmin(password: string): Promise<AdminLoginResponse> {
  return apiPost<AdminLoginResponse>("/admin/login", { password });
}

export async function logoutAdmin(token: string): Promise<AdminLogoutResponse> {
  return apiPost<AdminLogoutResponse>("/admin/logout", {}, { headers: authHeaders(token) });
}

export async function changeAdminPassword(
  token: string,
  currentPassword: string,
  newPassword: string
): Promise<AdminPasswordChangeResponse> {
  return apiPost<AdminPasswordChangeResponse>(
    "/admin/change-password",
    {
      current_password: currentPassword,
      new_password: newPassword
    },
    {
      headers: authHeaders(token)
    }
  );
}

export async function getAdminSettings(token: string): Promise<AdminSettingsResponse> {
  return apiGet<AdminSettingsResponse>("/admin/settings", { headers: authHeaders(token) });
}

export async function updateAdminSettings(
  token: string,
  payload: AdminSettingsUpdate
): Promise<AdminSettingsResponse> {
  return apiPut<AdminSettingsResponse>("/admin/settings", payload, {
    headers: authHeaders(token)
  });
}

export async function createFloorAsAdmin(token: string, name: string): Promise<Floor> {
  return apiPost<Floor>("/floors", { name }, { headers: authHeaders(token) });
}

export async function uploadFloorMapAsAdmin(token: string, floorId: string, file: File): Promise<Floor> {
  const data = new FormData();
  data.append("map_file", file);
  return apiPostForm<Floor>(`/floors/${encodeURIComponent(floorId)}/map/upload`, data, {
    headers: authHeaders(token)
  });
}