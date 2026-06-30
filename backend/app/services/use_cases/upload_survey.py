from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from app.api.schemas.survey import SurveyUploadResponse
from app.services.parsers.zip_parser import ParsedSurveyZip, SurveyZipParseError
from app.services.storage.blob_port import BlobPort
from app.services.storage.table_port import TablePort


class FloorNotFoundError(ValueError):
    pass


class InvalidSurveyPayloadError(ValueError):
    pass


@dataclass
class UploadSurveyRequest:
    floor_id: str
    x_norm: float
    y_norm: float
    filename: str
    payload: bytes


class UploadSurveyUseCase:
    def __init__(
        self,
        *,
        table_port: TablePort,
        blob_port: BlobPort,
        parse_zip: Callable[[bytes, str, float, float], ParsedSurveyZip],
    ) -> None:
        self._table_port = table_port
        self._blob_port = blob_port
        self._parse_zip = parse_zip

    def execute(self, request: UploadSurveyRequest) -> SurveyUploadResponse:
        if request.floor_id not in {floor.id for floor in self._table_port.list_floors()}:
            raise FloorNotFoundError("floor not found")

        self._blob_port.save_raw_upload(request.filename, request.payload)

        try:
            parsed_payload = self._parse_zip(
                request.payload,
                request.floor_id,
                request.x_norm,
                request.y_norm,
            )
        except SurveyZipParseError as exc:
            raise InvalidSurveyPayloadError(str(exc)) from exc

        session = self._table_port.add_survey_session(
            floor_id=request.floor_id,
            source_filename=request.filename,
            location_x_norm=request.x_norm,
            location_y_norm=request.y_norm,
            metadata=parsed_payload.metadata,
            networks_excerpt=parsed_payload.networks_excerpt,
            interface_excerpt=parsed_payload.interface_excerpt,
            log_files=parsed_payload.log_files,
        )
        self._table_port.add_readings(parsed_payload.readings)

        return SurveyUploadResponse(session=session, reading_count=len(parsed_payload.readings))
