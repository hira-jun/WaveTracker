export interface NormalizedPoint {
  xNorm: number;
  yNorm: number;
}

function clamp01(value: number): number {
  return Math.min(1, Math.max(0, value));
}

export function toNormalizedPoint(
  clickX: number,
  clickY: number,
  width: number,
  height: number
): NormalizedPoint {
  return {
    xNorm: clamp01(clickX / width),
    yNorm: clamp01(clickY / height)
  };
}
