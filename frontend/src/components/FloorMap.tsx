import type { SurveyReading } from "../types/survey";
import { toNormalizedPoint } from "../utils/coordinates";

interface FloorMapProps {
  onPointSelected: (point: { xNorm: number; yNorm: number }) => void;
  readings: SurveyReading[];
}

export function FloorMap({ onPointSelected, readings }: FloorMapProps) {
  return (
    <div>
      <p style={{ margin: "0 0 0.5rem 0" }}>Floor map (Phase0 placeholder canvas)</p>
      <div
        onClick={(event) => {
          const rect = event.currentTarget.getBoundingClientRect();
          const x = event.clientX - rect.left;
          const y = event.clientY - rect.top;
          onPointSelected(toNormalizedPoint(x, y, rect.width, rect.height));
        }}
        style={{
          position: "relative",
          width: "100%",
          height: "360px",
          border: "1px solid #bbb",
          borderRadius: "8px",
          background: "linear-gradient(140deg, #f5f7fb 0%, #e8edf7 100%)",
          cursor: "crosshair"
        }}
      >
        {readings.map((reading, index) => (
          <span
            key={`${reading.bssid}-${index}`}
            title={`${reading.ssid} (${reading.signal_dbm} dBm)`}
            style={{
              position: "absolute",
              left: `${reading.x_norm * 100}%`,
              top: `${reading.y_norm * 100}%`,
              width: "10px",
              height: "10px",
              borderRadius: "999px",
              backgroundColor: reading.signal_dbm >= -67 ? "#007a3d" : "#cc6f00",
              transform: "translate(-50%, -50%)"
            }}
          />
        ))}
      </div>
    </div>
  );
}
