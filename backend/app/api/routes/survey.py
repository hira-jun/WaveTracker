from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from app.api.schemas.survey import SurveyReading, SurveySession, SurveyUploadResponse
from app.services.dependencies import table_adapter, upload_survey_use_case
from app.services.use_cases.upload_survey import (
    FloorNotFoundError,
    InvalidSurveyPayloadError,
    UploadSurveyRequest,
)


router = APIRouter()


@router.post("/upload", response_model=SurveyUploadResponse)
async def upload_survey(
    floor_id: str = Query(..., min_length=1),
    x_norm: float = Query(..., ge=0, le=1),
    y_norm: float = Query(..., ge=0, le=1),
    upload: UploadFile = File(...),
) -> SurveyUploadResponse:
    payload = await upload.read()
    request = UploadSurveyRequest(
        floor_id=floor_id,
        x_norm=x_norm,
        y_norm=y_norm,
        filename=upload.filename or "survey.zip",
        payload=payload,
    )

    try:
        return upload_survey_use_case.execute(request)
    except FloorNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except InvalidSurveyPayloadError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


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
