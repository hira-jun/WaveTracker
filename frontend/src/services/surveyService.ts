import { apiGet, apiPost, apiPostForm } from "./apiClient";
import type {
  APBandSummaryResponse,
  Floor,
  HeatmapPoint,
  IssueReport,
  IssueReportCreate,
  SurveyReading,
  SurveySession,
  SurveyUploadResponse
} from "../types/survey";

interface HeatmapResponse {
  floor_id: string;
  points: HeatmapPoint[];
}

export async function listFloors(): Promise<Floor[]> {
  return apiGet<Floor[]>("/floors");
}

export async function createFloor(name: string): Promise<Floor> {
  return apiPost<Floor>("/floors", { name });
}

export async function uploadFloorMapFile(floorId: string, file: File): Promise<Floor> {
  const data = new FormData();
  data.append("map_file", file);
  return apiPostForm<Floor>(`/floors/${encodeURIComponent(floorId)}/map/upload`, data);
}

export async function listReadings(floorId: string): Promise<SurveyReading[]> {
  return apiGet<SurveyReading[]>(`/survey/readings?floor_id=${encodeURIComponent(floorId)}`);
}

export async function uploadSurveyZip(
  floorId: string,
  file: File,
  location: { xNorm: number; yNorm: number }
): Promise<SurveyUploadResponse> {
  const data = new FormData();
  data.append("upload", file);
  return apiPostForm<SurveyUploadResponse>(
    `/survey/upload?floor_id=${encodeURIComponent(floorId)}&x_norm=${encodeURIComponent(
      String(location.xNorm)
    )}&y_norm=${encodeURIComponent(String(location.yNorm))}`,
    data
  );
}

export async function listSurveySessions(floorId: string): Promise<SurveySession[]> {
  return apiGet<SurveySession[]>(`/survey/sessions?floor_id=${encodeURIComponent(floorId)}`);
}

export async function getSurveySession(sessionId: string): Promise<SurveySession> {
  return apiGet<SurveySession>(`/survey/sessions/${encodeURIComponent(sessionId)}`);
}

export async function getHeatmap(floorId: string): Promise<HeatmapPoint[]> {
  const response = await apiGet<HeatmapResponse>(`/analytics/heatmap?floor_id=${encodeURIComponent(floorId)}`);
  return response.points;
}

export async function getAPBandSummary(floorId: string): Promise<APBandSummaryResponse> {
  return apiGet<APBandSummaryResponse>(`/analytics/ap?floor_id=${encodeURIComponent(floorId)}`);
}

export async function createIssueReport(payload: IssueReportCreate): Promise<IssueReport> {
  return apiPost<IssueReport>("/issues", payload);
}

export async function listIssueReports(floorId: string): Promise<IssueReport[]> {
  return apiGet<IssueReport[]>(`/issues?floor_id=${encodeURIComponent(floorId)}`);
}
