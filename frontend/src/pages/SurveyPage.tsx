import { useEffect, useMemo, useState } from "react";

import { FloorMap } from "../components/FloorMap";
import { UploadPanel } from "../components/UploadPanel";
import {
  createIssueReport,
  getSurveySession,
  listFloors,
  listIssueReports,
  listReadings,
  listSurveySessions,
  uploadSurveyZip
} from "../services/surveyService";
import type {
  Floor,
  IssueReport,
  IssueSeverity,
  IssueType,
  SurveyReading,
  SurveySession,
  WifiBand
} from "../types/survey";

type BandFilter = "all" | WifiBand;

const bandOrder: WifiBand[] = ["2.4GHz", "5GHz", "6GHz"];

const bandColors: Record<WifiBand, string> = {
  "2.4GHz": "#7a5af8",
  "5GHz": "#1570ef",
  "6GHz": "#039855"
};

export function SurveyPage() {
  const [floors, setFloors] = useState<Floor[]>([]);
  const [selectedFloorId, setSelectedFloorId] = useState<string>("");
  const [readings, setReadings] = useState<SurveyReading[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedPoint, setSelectedPoint] = useState<{ xNorm: number; yNorm: number } | null>(null);
  const [sessions, setSessions] = useState<SurveySession[]>([]);
  const [selectedSessionId, setSelectedSessionId] = useState<string>("");
  const [selectedSession, setSelectedSession] = useState<SurveySession | null>(null);
  const [bandFilter, setBandFilter] = useState<BandFilter>("all");
  const [issues, setIssues] = useState<IssueReport[]>([]);
  const [issueSsid, setIssueSsid] = useState("");
  const [issueType, setIssueType] = useState<IssueType>("disconnect");
  const [issueSeverity, setIssueSeverity] = useState<IssueSeverity>("medium");

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError(null);

    listFloors()
      .then((result) => {
        if (!active) {
          return;
        }
        setFloors(result);
        if (result.length > 0) {
          setSelectedFloorId(result[0].id);
        }
      })
      .catch((loadError) => {
        if (active) {
          setError(loadError instanceof Error ? loadError.message : "Failed to load floors");
        }
      })
      .finally(() => {
        if (active) {
          setLoading(false);
        }
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (selectedFloorId.length === 0) {
      setReadings([]);
      setSessions([]);
      setSelectedSessionId("");
      setSelectedSession(null);
      return;
    }

    let active = true;
    Promise.all([
      listReadings(selectedFloorId),
      listSurveySessions(selectedFloorId),
      listIssueReports(selectedFloorId)
    ])
      .then(([readingResult, sessionResult, issueResult]) => {
        if (!active) {
          return;
        }
        setReadings(readingResult);
        setSessions(sessionResult);
        setIssues(issueResult);
        if (sessionResult.length > 0) {
          setSelectedSessionId(sessionResult[0].id);
        } else {
          setSelectedSessionId("");
          setSelectedSession(null);
        }
      })
      .catch((loadError) => {
        if (active) {
          setError(loadError instanceof Error ? loadError.message : "Failed to load readings");
        }
      });

    return () => {
      active = false;
    };
  }, [selectedFloorId]);

  useEffect(() => {
    if (selectedSessionId.length === 0) {
      setSelectedSession(null);
      return;
    }

    let active = true;
    getSurveySession(selectedSessionId)
      .then((session) => {
        if (active) {
          setSelectedSession(session);
        }
      })
      .catch((loadError) => {
        if (active) {
          setError(loadError instanceof Error ? loadError.message : "Failed to load session details");
        }
      });

    return () => {
      active = false;
    };
  }, [selectedSessionId]);

  const selectedFloor = useMemo(
    () => floors.find((floor) => floor.id === selectedFloorId) ?? null,
    [floors, selectedFloorId]
  );

  const bandSummary = useMemo(() => {
    const counts: Record<WifiBand, number> = {
      "2.4GHz": 0,
      "5GHz": 0,
      "6GHz": 0
    };
    for (const reading of readings) {
      counts[reading.band] += 1;
    }
    return counts;
  }, [readings]);

  const visibleReadings = useMemo(() => {
    if (bandFilter === "all") {
      return readings;
    }
    return readings.filter((reading) => reading.band === bandFilter);
  }, [readings, bandFilter]);

  return (
    <section style={{ display: "grid", gap: "1rem" }}>
      <h2 style={{ margin: 0 }}>Survey</h2>
      {loading && <p style={{ margin: 0 }}>Loading floors...</p>}
      {error && <p style={{ margin: 0, color: "#b42318" }}>{error}</p>}

      <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", alignItems: "center" }}>
        <label htmlFor="floor-select">Floor</label>
        <select
          id="floor-select"
          value={selectedFloorId}
          onChange={(event) => setSelectedFloorId(event.target.value)}
        >
          <option value="">Select floor</option>
          {floors.map((floor) => (
            <option key={floor.id} value={floor.id}>
              {floor.name}
            </option>
          ))}
        </select>
      </div>

      <p style={{ margin: 0, color: "#555" }}>
        Selected floor: {selectedFloor?.name ?? "none"}
      </p>
      <p style={{ margin: 0, color: "#555" }}>
        Map path: {selectedFloor?.map_image_url ?? "not uploaded"}
      </p>
      <section style={{ display: "grid", gap: "0.5rem" }}>
        <h3 style={{ margin: 0, fontSize: "1rem" }}>Band Filter</h3>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
          <button
            type="button"
            onClick={() => setBandFilter("all")}
            style={{
              border: bandFilter === "all" ? "2px solid #101828" : "1px solid #d0d5dd",
              borderRadius: "999px",
              padding: "0.25rem 0.65rem",
              backgroundColor: "#fff"
            }}
          >
            all
          </button>
          {bandOrder.map((band) => (
            <button
              key={`${band}-filter`}
              type="button"
              onClick={() => setBandFilter(band)}
              style={{
                border: bandFilter === band ? "2px solid #101828" : "1px solid #d0d5dd",
                borderRadius: "999px",
                padding: "0.25rem 0.65rem",
                backgroundColor: "#fff"
              }}
            >
              {band}
            </button>
          ))}
        </div>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
          {bandOrder.map((band) => (
            <span
              key={`${band}-summary`}
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "0.35rem",
                border: "1px solid #d0d5dd",
                borderRadius: "999px",
                padding: "0.25rem 0.65rem",
                fontSize: "0.9rem"
              }}
            >
              <span
                style={{
                  width: "10px",
                  height: "10px",
                  borderRadius: "999px",
                  backgroundColor: bandColors[band]
                }}
              />
              {band}: {bandSummary[band]}
            </span>
          ))}
        </div>
      </section>
      <FloorMap onPointSelected={setSelectedPoint} readings={visibleReadings} />
      <p style={{ margin: 0, color: "#555" }}>
        Visible readings: {visibleReadings.length}
      </p>
      <p style={{ margin: 0 }}>
        Click point: {selectedPoint ? `${selectedPoint.xNorm.toFixed(3)}, ${selectedPoint.yNorm.toFixed(3)}` : "not selected"}
      </p>

      <UploadPanel
        disabled={selectedFloorId.length === 0 || selectedPoint == null}
        selectedPoint={selectedPoint}
        onUpload={async (file, location) => {
          if (selectedFloorId.length === 0) {
            throw new Error("Select floor first");
          }
          const uploadResult = await uploadSurveyZip(selectedFloorId, file, location);
          setReadings(await listReadings(selectedFloorId));
          const reloadedSessions = await listSurveySessions(selectedFloorId);
          setSessions(reloadedSessions);
          setSelectedSessionId(uploadResult.session.id);
        }}
      />

      <section style={{ display: "grid", gap: "0.5rem" }}>
        <h3 style={{ margin: 0 }}>Issue report</h3>
        <p style={{ margin: 0, color: "#555" }}>
          Selected point: {selectedPoint ? `${selectedPoint.xNorm.toFixed(3)}, ${selectedPoint.yNorm.toFixed(3)}` : "not selected"}
        </p>
        <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", alignItems: "center" }}>
          <input
            type="text"
            value={issueSsid}
            onChange={(event) => setIssueSsid(event.target.value)}
            placeholder="SSID"
          />
          <select value={issueType} onChange={(event) => setIssueType(event.target.value as IssueType)}>
            <option value="connection_unavailable">connection unavailable</option>
            <option value="latency">latency</option>
            <option value="disconnect">disconnect</option>
            <option value="auth_failure">auth failure</option>
          </select>
          <select
            value={issueSeverity}
            onChange={(event) => setIssueSeverity(event.target.value as IssueSeverity)}
          >
            <option value="low">low</option>
            <option value="medium">medium</option>
            <option value="high">high</option>
          </select>
          <button
            type="button"
            disabled={selectedFloorId.length === 0 || selectedPoint == null || issueSsid.trim().length === 0}
            onClick={async () => {
              if (selectedPoint == null || selectedFloorId.length === 0) {
                return;
              }
              setError(null);
              try {
                const created = await createIssueReport({
                  floor_id: selectedFloorId,
                  x_norm: selectedPoint.xNorm,
                  y_norm: selectedPoint.yNorm,
                  occurred_at: new Date().toISOString(),
                  ssid: issueSsid,
                  issue_type: issueType,
                  severity: issueSeverity
                });
                setIssues((previous) => [created, ...previous]);
                setIssueSsid("");
              } catch (issueError) {
                setError(issueError instanceof Error ? issueError.message : "Failed to create issue report");
              }
            }}
          >
            Add issue
          </button>
        </div>
        <p style={{ margin: 0 }}>Issue count: {issues.length}</p>
        <ul style={{ margin: 0, paddingInlineStart: "1.2rem" }}>
          {issues.slice(0, 8).map((issue) => (
            <li key={issue.id}>
              {issue.issue_type} / {issue.severity} / {issue.ssid} @ {issue.x_norm.toFixed(2)}, {issue.y_norm.toFixed(2)}
            </li>
          ))}
        </ul>
      </section>

      <section style={{ display: "grid", gap: "0.5rem" }}>
        <h3 style={{ margin: 0 }}>Survey sessions</h3>
        <div style={{ display: "flex", gap: "0.5rem", alignItems: "center", flexWrap: "wrap" }}>
          <label htmlFor="session-select">Session</label>
          <select
            id="session-select"
            value={selectedSessionId}
            onChange={(event) => setSelectedSessionId(event.target.value)}
          >
            <option value="">Select session</option>
            {sessions.map((session) => (
              <option key={session.id} value={session.id}>
                {session.source_filename} ({new Date(session.captured_at).toLocaleString()})
              </option>
            ))}
          </select>
          <span>Count: {sessions.length}</span>
        </div>
        {selectedSession && (
          <div style={{ border: "1px solid #ddd", borderRadius: "8px", padding: "0.75rem", display: "grid", gap: "0.25rem" }}>
            <strong>Latest session details</strong>
            <span>Source: {selectedSession.source_filename}</span>
            <span>
              Upload location: {
                selectedSession.location_x_norm != null && selectedSession.location_y_norm != null
                  ? `${selectedSession.location_x_norm.toFixed(3)}, ${selectedSession.location_y_norm.toFixed(3)}`
                  : "n/a"
              }
            </span>
            <span>Logs: {selectedSession.log_files.length}</span>
            <span>
              Metadata keys: {Object.keys(selectedSession.metadata ?? {}).length}
            </span>
            <span>
              Networks excerpt: {(selectedSession.networks_excerpt ?? "").slice(0, 80) || "n/a"}
            </span>
            <span>
              Interface excerpt: {(selectedSession.interface_excerpt ?? "").slice(0, 80) || "n/a"}
            </span>
          </div>
        )}
      </section>
    </section>
  );
}
