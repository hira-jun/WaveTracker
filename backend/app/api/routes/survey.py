from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from app.api.schemas.survey import SurveyReading, SurveySession, SurveyUploadResponse
from app.services.parsers.zip_parser import SurveyZipParseError, parse_survey_zip
from app.services.dependencies import blob_adapter, table_adapter


router = APIRouter()


@router.post("/upload", response_model=SurveyUploadResponse)
async def upload_survey(
    floor_id: str = Query(..., min_length=1),
    x_norm: float = Query(..., ge=0, le=1),
    y_norm: float = Query(..., ge=0, le=1),
    upload: UploadFile = File(...),
) -> SurveyUploadResponse:
    if floor_id not in {floor.id for floor in table_adapter.list_floors()}:
        raise HTTPException(status_code=404, detail="floor not found")

    payload = await upload.read()
    blob_adapter.save_raw_upload(upload.filename or "survey.zip", payload)

    try:
        parsed_payload = parse_survey_zip(
            payload,
            floor_id=floor_id,
            fallback_x_norm=x_norm,
            fallback_y_norm=y_norm,
        )
    except SurveyZipParseError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    session = table_adapter.add_survey_session(
        floor_id=floor_id,
        source_filename=upload.filename or "survey.zip",
        location_x_norm=x_norm,
        location_y_norm=y_norm,
        metadata=parsed_payload.metadata,
        networks_excerpt=parsed_payload.networks_excerpt,
        interface_excerpt=parsed_payload.interface_excerpt,
        log_files=parsed_payload.log_files,
    )
    table_adapter.add_readings(parsed_payload.readings)

    return SurveyUploadResponse(session=session, reading_count=len(parsed_payload.readings))


@router.get("/readings", response_model=list[SurveyReading])
def get_readings(floor_id: str | None = Query(default=None)) -> list[SurveyReading]:
    return table_adapter.get_readings(floor_id=floor_id)


@router.get("/sessions", response_model=list[SurveySession])
def list_sessions(floor_id: str | None = Query(default=None)) -> list[SurveySession]:
    return table_adapter.list_survey_sessions(floor_id=floor_id)


@router.get("/sessions/{session_id}", response_model=SurveySession)
def get_session(session_id: str) -> SurveySession:
    session = table_adapter.get_survey_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session not found")
    return session
