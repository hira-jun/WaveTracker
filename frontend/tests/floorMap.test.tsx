import { act } from "react";
import { createRoot, Root } from "react-dom/client";
import { afterEach, describe, expect, it, vi } from "vitest";

import { FloorMap } from "../src/components/FloorMap";
import type { SurveyReading } from "../src/types/survey";

let root: Root | null = null;
let container: HTMLDivElement | null = null;

afterEach(() => {
  if (root) {
    act(() => {
      root?.unmount();
    });
  }
  root = null;

  if (container && container.parentNode) {
    container.parentNode.removeChild(container);
  }
  container = null;
});

function renderMap(onPointSelected = vi.fn(), readings: SurveyReading[] = []) {
  container = document.createElement("div");
  document.body.appendChild(container);
  root = createRoot(container);

  act(() => {
    root?.render(<FloorMap onPointSelected={onPointSelected} readings={readings} />);
  });

  const canvas = container.querySelector('[data-testid="floor-map-canvas"]') as HTMLDivElement;
  return { canvas, onPointSelected };
}

describe("FloorMap", () => {
  it("converts click position to normalized coordinates", () => {
    const { canvas, onPointSelected } = renderMap();

    vi.spyOn(canvas, "getBoundingClientRect").mockReturnValue({
      x: 10,
      y: 20,
      width: 400,
      height: 200,
      top: 20,
      right: 410,
      bottom: 220,
      left: 10,
      toJSON: () => ({})
    } as DOMRect);

    act(() => {
      canvas.dispatchEvent(
        new MouseEvent("click", {
          bubbles: true,
          clientX: 210,
          clientY: 120
        })
      );
    });

    expect(onPointSelected).toHaveBeenCalledTimes(1);
    expect(onPointSelected).toHaveBeenCalledWith({ xNorm: 0.5, yNorm: 0.5 });
  });

  it("renders reading point markers at expected positions", () => {
    const readings: SurveyReading[] = [
      {
        floor_id: "floor-1",
        x_norm: 0.25,
        y_norm: 0.75,
        ssid: "ANET",
        bssid: "aa:bb:cc:dd:ee:ff",
        band: "5GHz",
        channel: 44,
        signal_dbm: -60,
        captured_at: "2026-07-01T00:00:00Z"
      }
    ];

    renderMap(vi.fn(), readings);

    const marker = container?.querySelector('[title="ANET (-60 dBm)"]') as HTMLSpanElement;
    expect(marker).toBeTruthy();
    expect(marker.style.left).toBe("25%");
    expect(marker.style.top).toBe("75%");
  });
});
