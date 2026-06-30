from typing import Literal


WifiBand = Literal["2.4GHz", "5GHz", "6GHz"]

WIFI_BANDS: tuple[WifiBand, WifiBand, WifiBand] = ("2.4GHz", "5GHz", "6GHz")


def _to_float(value: object) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_band(
    band_hint: object,
    *,
    channel: int | None = None,
    frequency_mhz: float | None = None,
) -> WifiBand:
    text = str(band_hint or "").strip().lower()

    if frequency_mhz is not None:
        if frequency_mhz >= 5925:
            return "6GHz"
        if frequency_mhz >= 5000:
            return "5GHz"
        return "2.4GHz"

    if "6ghz" in text or "6 ghz" in text or "6g" in text:
        return "6GHz"
    if "5ghz" in text or "5 ghz" in text or "5g" in text:
        return "5GHz"
    if "2.4ghz" in text or "2.4 ghz" in text or "2g" in text:
        return "2.4GHz"

    numeric_in_text = _to_float(text.replace("mhz", "").strip())
    if numeric_in_text is not None:
        if numeric_in_text >= 5925:
            return "6GHz"
        if numeric_in_text >= 5000:
            return "5GHz"
        return "2.4GHz"

    if channel is not None:
        if channel <= 14:
            return "2.4GHz"
        if channel >= 181:
            return "6GHz"
        return "5GHz"

    return "5GHz"
