import json

from app.services.parsers.zip_parser import SurveyZipParseError, parse_survey_zip


def test_parse_survey_zip_extracts_readings(zip_payload_builder) -> None:
    payload = zip_payload_builder(
        {
            "metadata.json": json.dumps({"collector": "windows"}),
            "scan.json": json.dumps(
                {
                    "readings": [
                        {
                            "xNorm": 0.25,
                            "yNorm": 0.75,
                            "ssid": "ANET",
                            "bssid": "aa:bb:cc:dd:ee:ff",
                            "band": "5GHz",
                            "channel": 44,
                            "signal": -62,
                            "capturedAt": "2026-06-30T12:00:00Z",
                        }
                    ]
                }
            ),
            "networks.txt": "sample",
            "interface.txt": "sample",
            "logs/wlan.log": "sample",
        }
    )

    parsed = parse_survey_zip(payload, floor_id="floor-1")
    assert parsed.metadata["collector"] == "windows"
    assert isinstance(parsed.metadata, dict)
    assert len(parsed.readings) == 1
    assert parsed.readings[0].floor_id == "floor-1"
    assert parsed.readings[0].signal_dbm == -62
    assert "sample" in parsed.networks_excerpt
    assert "sample" in parsed.interface_excerpt
    assert parsed.log_files == ["logs/wlan.log"]


def test_parse_survey_zip_normalizes_6ghz_band(zip_payload_builder) -> None:
    payload = zip_payload_builder(
        {
            "metadata.json": json.dumps({"collector": "windows"}),
            "scan.json": json.dumps(
                {
                    "readings": [
                        {
                            "xNorm": 0.5,
                            "yNorm": 0.5,
                            "ssid": "ANET-6",
                            "bssid": "11:22:33:44:55:66",
                            "frequency": 6115,
                            "channel": 181,
                            "signal": -58,
                            "capturedAt": "2026-06-30T12:05:00Z",
                        }
                    ]
                }
            ),
            "networks.txt": "sample",
            "interface.txt": "sample",
            "logs/wlan.log": "sample",
        }
    )

    parsed = parse_survey_zip(payload, floor_id="floor-6")
    assert parsed.readings[0].band == "6GHz"


def test_parse_survey_zip_uses_fallback_location_when_missing(zip_payload_builder) -> None:
    payload = zip_payload_builder(
        {
            "metadata.json": json.dumps({"collector": "windows"}),
            "scan.json": json.dumps(
                {
                    "readings": [
                        {
                            "ssid": "ANET",
                            "bssid": "aa:bb:cc:dd:ee:ff",
                            "channel": 11,
                            "signal": -70,
                            "capturedAt": "2026-06-30T12:00:00Z",
                        }
                    ]
                }
            ),
            "networks.txt": "sample",
            "interface.txt": "sample",
            "logs/wlan.log": "sample",
        }
    )

    parsed = parse_survey_zip(payload, floor_id="floor-1", fallback_x_norm=0.15, fallback_y_norm=0.85)
    assert parsed.readings[0].x_norm == 0.15
    assert parsed.readings[0].y_norm == 0.85


def test_parse_survey_zip_requires_logs_and_files(zip_payload_builder) -> None:
    payload = zip_payload_builder(
        {
            "metadata.json": json.dumps({"collector": "windows"}),
            "scan.json": json.dumps({"readings": []}),
            "networks.txt": "sample",
            "interface.txt": "sample",
        }
    )

    try:
        parse_survey_zip(payload, floor_id="floor-1")
        assert False, "expected SurveyZipParseError"
    except SurveyZipParseError as exc:
        assert "missing logs" in str(exc)
