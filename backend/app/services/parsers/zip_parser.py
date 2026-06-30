from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from io import BytesIO
from zipfile import BadZipFile, ZipFile

from app.api.schemas.survey import SurveyReading
from app.domain.wifi_bands import normalize_band


REQUIRED_FILES = {
    "metadata.json",
    "scan.json",
    "networks.txt",
    "interface.txt",
}


class SurveyZipParseError(ValueError):
    pass


@dataclass
class ParsedSurveyZip:
    metadata: dict
    readings: list[SurveyReading]
    networks_excerpt: str
    interface_excerpt: str
    log_files: list[str]


def _coalesce(mapping: dict, keys: list[str], default=None):
    for key in keys:
        if key in mapping:
            return mapping[key]
    return default


def _parse_datetime(value: object) -> datetime:
    if not isinstance(value, str) or not value:
        return datetime.now(UTC)
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.now(UTC)


def _extract_entries(scan_data: object) -> list[dict]:
    if isinstance(scan_data, list):
        return [item for item in scan_data if isinstance(item, dict)]

    if isinstance(scan_data, dict):
        candidates = [
            _coalesce(scan_data, ["readings", "entries", "networks", "results"], default=[])
        ]
        for candidate in candidates:
            if isinstance(candidate, list):
                return [item for item in candidate if isinstance(item, dict)]

    return []


def _to_float(value: object, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value: object, default: int) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _build_reading(
    entry: dict,
    floor_id: str,
    fallback_x_norm: float = 0.5,
    fallback_y_norm: float = 0.5,
) -> SurveyReading:
    x_norm = _to_float(_coalesce(entry, ["x_norm", "xNorm", "x", "xRatio"]), fallback_x_norm)
    y_norm = _to_float(_coalesce(entry, ["y_norm", "yNorm", "y", "yRatio"]), fallback_y_norm)
    channel = _to_int(_coalesce(entry, ["channel", "ch"], default=0), 0)
    frequency_mhz = _to_float(
        _coalesce(entry, ["frequency_mhz", "frequencyMHz", "frequency", "freq_mhz", "freq"]),
        0,
    )

    x_norm = max(0.0, min(1.0, x_norm))
    y_norm = max(0.0, min(1.0, y_norm))

    return SurveyReading(
        floor_id=floor_id,
        x_norm=x_norm,
        y_norm=y_norm,
        ssid=str(_coalesce(entry, ["ssid", "SSID"], default="unknown-ssid")),
        bssid=str(_coalesce(entry, ["bssid", "BSSID"], default="00:00:00:00:00:00")),
        band=normalize_band(
            _coalesce(entry, ["band", "frequencyBand", "band_hint", "radio"]),
            channel=channel,
            frequency_mhz=frequency_mhz if frequency_mhz > 0 else None,
        ),
        channel=channel,
        signal_dbm=_to_int(_coalesce(entry, ["signal_dbm", "signal", "rssi", "dbm"], default=-90), -90),
        captured_at=_parse_datetime(_coalesce(entry, ["captured_at", "capturedAt", "timestamp"])),
    )


def parse_survey_zip(
    payload: bytes,
    floor_id: str,
    fallback_x_norm: float = 0.5,
    fallback_y_norm: float = 0.5,
) -> ParsedSurveyZip:
    try:
        with ZipFile(BytesIO(payload)) as archive:
            names = set(archive.namelist())
            missing = sorted(REQUIRED_FILES - names)
            has_logs = any(name.startswith("logs/") for name in names)
            if missing:
                raise SurveyZipParseError(f"missing required files: {', '.join(missing)}")
            if not has_logs:
                raise SurveyZipParseError("missing logs directory entries")

            metadata_raw = archive.read("metadata.json")
            scan_raw = archive.read("scan.json")
            networks_raw = archive.read("networks.txt")
            interface_raw = archive.read("interface.txt")
            log_files = sorted(name for name in names if name.startswith("logs/") and not name.endswith("/"))

    except BadZipFile as exc:
        raise SurveyZipParseError("invalid zip format") from exc
    except KeyError as exc:
        raise SurveyZipParseError("zip payload missing required members") from exc

    try:
        metadata = json.loads(metadata_raw.decode("utf-8"))
        scan_data = json.loads(scan_raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise SurveyZipParseError("metadata.json or scan.json is not valid UTF-8 JSON") from exc

    entries = _extract_entries(scan_data)
    readings = [
        _build_reading(
            entry,
            floor_id=floor_id,
            fallback_x_norm=fallback_x_norm,
            fallback_y_norm=fallback_y_norm,
        )
        for entry in entries
    ]

    if not readings:
        raise SurveyZipParseError("scan.json contains no usable readings")

    if not isinstance(metadata, dict):
        raise SurveyZipParseError("metadata.json must be a JSON object")

    networks_excerpt = networks_raw.decode("utf-8", errors="replace")[:4000]
    interface_excerpt = interface_raw.decode("utf-8", errors="replace")[:4000]

    return ParsedSurveyZip(
        metadata=metadata,
        readings=readings,
        networks_excerpt=networks_excerpt,
        interface_excerpt=interface_excerpt,
        log_files=log_files,
    )
