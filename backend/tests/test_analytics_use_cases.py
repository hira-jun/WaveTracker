from datetime import UTC, datetime

from app.api.schemas.survey import SurveyReading
from app.services.storage.local_table_adapter import LocalTableAdapter
from app.services.use_cases.analytics import GetAPSummaryUseCase, GetHeatmapUseCase, GetIssueSummaryUseCase


def test_get_heatmap_use_case_maps_levels_and_bands() -> None:
    table = LocalTableAdapter()
    floor = table.create_floor("A")
    table.add_readings(
        [
            SurveyReading(
                floor_id=floor.id,
                x_norm=0.5,
                y_norm=0.5,
                ssid="ssid",
                bssid="aa:bb:cc:dd:ee:ff",
                band="5GHz",
                channel=36,
                signal_dbm=-60,
                captured_at=datetime.now(UTC),
            )
        ]
    )

    response = GetHeatmapUseCase(table_port=table).execute(floor_id=floor.id)

    assert response.floor_id == floor.id
    assert len(response.points) == 1
    assert response.points[0].band == "5GHz"


def test_get_ap_summary_use_case_groups_by_band() -> None:
    table = LocalTableAdapter()
    floor = table.create_floor("A")
    table.add_readings(
        [
            SurveyReading(
                floor_id=floor.id,
                x_norm=0.1,
                y_norm=0.1,
                ssid="s1",
                bssid="00:00:00:00:00:01",
                band="2.4GHz",
                channel=1,
                signal_dbm=-70,
                captured_at=datetime.now(UTC),
            ),
            SurveyReading(
                floor_id=floor.id,
                x_norm=0.2,
                y_norm=0.2,
                ssid="s2",
                bssid="00:00:00:00:00:02",
                band="5GHz",
                channel=44,
                signal_dbm=-65,
                captured_at=datetime.now(UTC),
            ),
        ]
    )

    response = GetAPSummaryUseCase(table_port=table).execute(floor_id=floor.id)
    counts = {item.band: item.count for item in response.by_band}

    assert counts["2.4GHz"] == 1
    assert counts["5GHz"] == 1


def test_get_issue_summary_use_case_returns_table_summary() -> None:
    table = LocalTableAdapter()
    floor = table.create_floor("A")

    response = GetIssueSummaryUseCase(table_port=table).execute(floor_id=floor.id)

    assert response.floor_id == floor.id
    assert response.issue_count == 0
