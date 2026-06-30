export interface Floor {
  id: string;
  name: string;
  map_image_url?: string | null;
}

export interface SurveyReading {
  floor_id: string;
  x_norm: number;
  y_norm: number;
  ssid: string;
  bssid: string;
  band: "2.4GHz" | "5GHz" | "6GHz";
  channel: number;
  signal_dbm: number;
  captured_at: string;
}

export type RssiLevel = "excellent" | "good" | "minimum" | "weak" | "unstable";

export interface HeatmapPoint {
  x_norm: number;
  y_norm: number;
  signal_dbm: number;
  level: RssiLevel;
  band: WifiBand;
}

export type WifiBand = "2.4GHz" | "5GHz" | "6GHz";

export interface BandSummary {
  band: WifiBand;
  count: number;
}

export interface APBandSummaryResponse {
  floor_id: string;
  by_band: BandSummary[];
}

export interface SurveySession {
  id: string;
  floor_id: string;
  captured_at: string;
  source_filename: string;
  location_x_norm?: number | null;
  location_y_norm?: number | null;
  metadata: Record<string, unknown>;
  networks_excerpt?: string | null;
  interface_excerpt?: string | null;
  log_files: string[];
}

export interface SurveyUploadResponse {
  session: SurveySession;
  reading_count: number;
}

export type IssueType = "connection_unavailable" | "latency" | "disconnect" | "auth_failure";
export type IssueSeverity = "low" | "medium" | "high";

export interface IssueReport {
  id: string;
  floor_id: string;
  x_norm: number;
  y_norm: number;
  occurred_at: string;
  ssid: string;
  issue_type: IssueType;
  severity: IssueSeverity;
}

export interface IssueReportCreate {
  floor_id: string;
  x_norm: number;
  y_norm: number;
  occurred_at: string;
  ssid: string;
  issue_type: IssueType;
  severity: IssueSeverity;
}
