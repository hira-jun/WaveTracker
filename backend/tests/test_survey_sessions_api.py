import json

from fastapi.testclient import TestClient

from app.main import app
from app.services.dependencies import table_adapter


def test_list_sessions_by_floor() -> None:
    floor = table_adapter.create_floor("Session Test Floor")
    table_adapter.add_survey_session(
        floor_id=floor.id,
        source_filename="sample.zip",
        metadata={"collector": "windows"},
        networks_excerpt="n1",
        interface_excerpt="i1",
        log_files=["logs/wlan.log"],
    )

    client = TestClient(app)
    response = client.get(f"/survey/sessions?floor_id={floor.id}")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 1
    assert payload[-1]["floor_id"] == floor.id


def test_get_session_detail_not_found() -> None:
    client = TestClient(app)
    response = client.get("/survey/sessions/session-does-not-exist")
    assert response.status_code == 404


def test_upload_survey_persists_selected_location(zip_payload_builder) -> None:
    floor = table_adapter.create_floor("Upload Location Floor")
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
                            "signal": -63,
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

    client = TestClient(app)
    response = client.post(
        f"/survey/upload?floor_id={floor.id}&x_norm=0.25&y_norm=0.75",
        files={"upload": ("sample.zip", payload, "application/zip")},
    )

    assert response.status_code == 200
    payload_json = response.json()
    assert payload_json["session"]["floor_id"] == floor.id
    assert payload_json["session"]["location_x_norm"] == 0.25
    assert payload_json["session"]["location_y_norm"] == 0.75
