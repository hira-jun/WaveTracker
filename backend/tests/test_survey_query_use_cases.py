import pytest

from app.api.schemas.survey import SurveyReading
from app.services.storage.local_table_adapter import LocalTableAdapter
from app.services.use_cases.survey_queries import (
    GetSurveySessionUseCase,
    ListSurveyReadingsUseCase,
    ListSurveySessionsUseCase,
    SurveySessionNotFoundError,
)


def test_list_survey_sessions_use_case_filters_by_floor() -> None:
    table = LocalTableAdapter()
    floor_a = table.create_floor("A")
    floor_b = table.create_floor("B")

    table.add_survey_session(floor_id=floor_a.id, source_filename="a.zip")
    table.add_survey_session(floor_id=floor_b.id, source_filename="b.zip")

    use_case = ListSurveySessionsUseCase(table_port=table)
    sessions = use_case.execute(floor_id=floor_a.id)

    assert len(sessions) == 1
    assert sessions[0].floor_id == floor_a.id


def test_get_survey_session_use_case_raises_when_missing() -> None:
    table = LocalTableAdapter()
    use_case = GetSurveySessionUseCase(table_port=table)

    with pytest.raises(SurveySessionNotFoundError):
        use_case.execute(session_id="missing-session")


def test_list_survey_readings_use_case_filters_by_floor() -> None:
    table = LocalTableAdapter()
    floor_a = table.create_floor("A")
    floor_b = table.create_floor("B")

    session_a = table.add_survey_session(floor_id=floor_a.id, source_filename="a.zip")
    session_b = table.add_survey_session(floor_id=floor_b.id, source_filename="b.zip")

    table.add_readings(
        [
            SurveyReading(
                floor_id=session_a.floor_id,
                x_norm=0.1,
                y_norm=0.2,
                ssid="ssid-a",
                bssid="aa:aa:aa:aa:aa:aa",
                band="2.4GHz",
                channel=1,
                signal_dbm=-60,
                captured_at=session_a.captured_at,
            )
        ]
    )
    table.add_readings(
        [
            SurveyReading(
                floor_id=session_b.floor_id,
                x_norm=0.3,
                y_norm=0.4,
                ssid="ssid-b",
                bssid="bb:bb:bb:bb:bb:bb",
                band="5GHz",
                channel=36,
                signal_dbm=-55,
                captured_at=session_b.captured_at,
            )
        ]
    )

    use_case = ListSurveyReadingsUseCase(table_port=table)
    readings = use_case.execute(floor_id=floor_a.id)

    assert len(readings) == 1
    assert readings[0].floor_id == floor_a.id
