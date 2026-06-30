export interface AdminStatusResponse {
  initialized: boolean;
}

export interface AdminLoginResponse {
  token: string;
}

export interface AdminLogoutResponse {
  logged_out: boolean;
}

export interface AdminPasswordChangeResponse {
  changed: boolean;
}

export interface AdminSettings {
  dashboard_title: string;
  default_floor_id: string | null;
  maintenance_message: string | null;
}

export interface AdminSettingsResponse {
  settings: AdminSettings;
}

export interface AdminSettingsUpdate {
  dashboard_title?: string;
  default_floor_id?: string | null;
  maintenance_message?: string | null;
}