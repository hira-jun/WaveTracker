import { describe, expect, it } from "vitest";

import { toNormalizedPoint } from "../src/utils/coordinates";

describe("coordinates", () => {
  it("normalizes click coordinates in map bounds", () => {
    const point = toNormalizedPoint(200, 90, 400, 180);

    expect(point).toEqual({ xNorm: 0.5, yNorm: 0.5 });
  });

  it("clamps values to range when click exceeds bounds", () => {
    const point = toNormalizedPoint(-20, 500, 400, 180);

    expect(point).toEqual({ xNorm: 0, yNorm: 1 });
  });
});
