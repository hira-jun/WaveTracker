from datetime import UTC, datetime

import pytest

from app.api.schemas.survey import SurveyReading
from app.services.parsers.zip_parser import ParsedSurveyZip, SurveyZipParseError
from app.services.storage.local_blob_adapter import LocalBlobAdapter
from app.services.storage.local_table_adapter import LocalTableAdapter
from app.services.use_cases.upload_survey import (
    FloorNotFoundError,
    InvalidSurveyPayloadError,
    UploadSurveyRequest,
    UploadSurveyUseCase,
)


def _build_parsed_payload(floor_id: str) -> ParsedSurveyZip:
    return ParsedSurveyZip(
        metadata={"collector": "test"},
        readings=[
            SurveyReading(
                floor_id=floor_id,
                x_norm=0.25,
                y_norm=0.75,
                ssid="TestSSID",
                bssid="aa:bb:cc:dd:ee:ff",
                band="5GHz",
                channel=44,
                signal_dbm=-57,
                captured_at=datetime.now(UTC),
            )
        ],
        networks_excerpt="n",
        interface_excerpt="i",
        log_files=["logs/test.log"],
    )


def test_execute_upload_survey_success(tmp_path) -> None:
    table = LocalTableAdapter()
    blob = LocalBlobAdapter(base_dir=tmp_path)
    floor = table.create_floor("Use Case Floor")

    use_case = UploadSurveyUseCase(
        table_port=table,
        blob_port=blob,
        parse_zip=lambda payload, floor_id, x_norm, y_norm: _build_parsed_payload(floor_id),
    )

    response = use_case.execute(
        UploadSurveyRequest(
            floor_id=floor.id,
            x_norm=0.4,
            y_norm=0.6,
            filename="survey.zip",
            payload=b"zip-content",
        )
    )

    assert response.reading_count == 1
    assert response.session.floor_id == floor.id
    assert response.session.location_x_norm == 0.4
    assert response.session.location_y_norm == 0.6
    assert (tmp_path / "survey.zip").exists()


def test_execute_upload_survey_floor_not_found(tmp_path) -> None:
    table = LocalTableAdapter()
    blob = LocalBlobAdapter(base_dir=tmp_path)

    use_case = UploadSurveyUseCase(
        table_port=table,
        blob_port=blob,
        parse_zip=lambda payload, floor_id, x_norm, y_norm: _build_parsed_payload(floor_id),
    )

    with pytest.raises(FloorNotFoundError):
        use_case.execute(
            UploadSurveyRequest(
                floor_id="missing-floor",
                x_norm=0.5,
                y_norm=0.5,
                filename="survey.zip",
                payload=b"zip-content",
            )
        )


def test_execute_upload_survey_invalid_payload(tmp_path) -> None:
    table = LocalTableAdapter()
    blob = LocalBlobAdapter(base_dir=tmp_path)
    floor = table.create_floor("Broken Payload Floor")

    def _raise_parse_error(payload, floor_id, x_norm, y_norm):
        raise SurveyZipParseError("invalid zip")

    use_case = UploadSurveyUseCase(
        table_port=table,
        blob_port=blob,
        parse_zip=_raise_parse_error,
    )

    with pytest.raises(InvalidSurveyPayloadError):
        use_case.execute(
            UploadSurveyRequest(
                floor_id=floor.id,
                x_norm=0.5,
                y_norm=0.5,
                filename="survey.zip",
                payload=b"broken",
            )
        )
