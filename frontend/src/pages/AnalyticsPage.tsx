import { useMemo, useState } from "react";

import { getAPBandSummary, getHeatmap } from "../services/surveyService";
import type { HeatmapPoint, RssiLevel, WifiBand } from "../types/survey";

const levelOrder: RssiLevel[] = ["excellent", "good", "minimum", "weak", "unstable"];

const levelColors: Record<RssiLevel, string> = {
  excellent: "#067647",
  good: "#0e9384",
  minimum: "#475467",
  weak: "#b54708",
  unstable: "#b42318"
};

const bandOrder: WifiBand[] = ["2.4GHz", "5GHz", "6GHz"];

const bandColors: Record<WifiBand, string> = {
  "2.4GHz": "#7a5af8",
  "5GHz": "#1570ef",
  "6GHz": "#039855"
};

type BandFilter = "all" | WifiBand;

export function AnalyticsPage() {
  const [floorId, setFloorId] = useState("");
  const [points, setPoints] = useState<HeatmapPoint[]>([]);
  const [bandFilter, setBandFilter] = useState<BandFilter>("all");
  const [bandSummary, setBandSummary] = useState<Record<WifiBand, number>>({
    "2.4GHz": 0,
    "5GHz": 0,
    "6GHz": 0
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const levelSummary = useMemo(() => {
    const counts: Record<RssiLevel, number> = {
      excellent: 0,
      good: 0,
      minimum: 0,
      weak: 0,
      unstable: 0
    };

    for (const point of points) {
      if (bandFilter !== "all" && point.band !== bandFilter) {
        continue;
      }
      counts[point.level] += 1;
    }

    return counts;
  }, [points, bandFilter]);

  const visiblePoints = useMemo(() => {
    if (bandFilter === "all") {
      return points;
    }
    return points.filter((point) => point.band === bandFilter);
  }, [points, bandFilter]);

  return (
    <section style={{ display: "grid", gap: "1rem" }}>
      <h2 style={{ margin: 0 }}>Analytics</h2>
      <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
        <input
          type="text"
          value={floorId}
          placeholder="floor id"
          onChange={(event) => setFloorId(event.target.value)}
        />
        <button
          type="button"
          disabled={floorId.length === 0 || loading}
          onClick={async () => {
            setLoading(true);
            setError(null);
            try {
              const [heatmapPoints, apSummary] = await Promise.all([
                getHeatmap(floorId),
                getAPBandSummary(floorId)
              ]);
              setPoints(heatmapPoints);
              setBandFilter("all");
              const nextSummary: Record<WifiBand, number> = {
                "2.4GHz": 0,
                "5GHz": 0,
                "6GHz": 0
              };
              for (const item of apSummary.by_band) {
                nextSummary[item.band] = item.count;
              }
              setBandSummary(nextSummary);
            } catch (analyticsError) {
              setError(analyticsError instanceof Error ? analyticsError.message : "Failed to load analytics");
            } finally {
              setLoading(false);
            }
          }}
        >
          {loading ? "Loading..." : "Load heatmap"}
        </button>
      </div>

      {error && <p style={{ margin: 0, color: "#b42318" }}>{error}</p>}
      <p style={{ margin: 0 }}>Heatmap points: {visiblePoints.length}</p>
      <section style={{ display: "grid", gap: "0.5rem" }}>
        <h3 style={{ margin: 0, fontSize: "1rem" }}>Band Summary</h3>
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
              key={band}
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
      <section style={{ display: "grid", gap: "0.5rem" }}>
        <h3 style={{ margin: 0, fontSize: "1rem" }}>RSSI Summary</h3>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
          {levelOrder.map((level) => (
            <span
              key={level}
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
                  backgroundColor: levelColors[level]
                }}
              />
              {level}: {levelSummary[level]}
            </span>
          ))}
        </div>
      </section>
      <ul style={{ margin: 0, paddingInlineStart: "1.2rem" }}>
        {visiblePoints.slice(0, 10).map((point, index) => (
          <li key={`${point.x_norm}-${point.y_norm}-${index}`}>
            {point.band} / {point.level} ({point.signal_dbm} dBm) at {point.x_norm.toFixed(2)}, {point.y_norm.toFixed(2)}
          </li>
        ))}
      </ul>
    </section>
  );
}
