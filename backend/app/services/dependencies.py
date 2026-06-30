from fastapi import Header, HTTPException

from app.services.admin_auth import AdminAuthService
from app.services.parsers.zip_parser import parse_survey_zip
from app.services.storage.local_blob_adapter import LocalBlobAdapter
from app.services.storage.local_table_adapter import LocalTableAdapter
from app.services.use_cases.survey_queries import (
	GetSurveySessionUseCase,
	ListSurveyReadingsUseCase,
	ListSurveySessionsUseCase,
)
from app.services.use_cases.upload_survey import UploadSurveyUseCase


table_adapter = LocalTableAdapter()
blob_adapter = LocalBlobAdapter()
admin_auth = AdminAuthService()
upload_survey_use_case = UploadSurveyUseCase(
    table_port=table_adapter,
    blob_port=blob_adapter,
    parse_zip=parse_survey_zip,
)
list_survey_sessions_use_case = ListSurveySessionsUseCase(table_port=table_adapter)
get_survey_session_use_case = GetSurveySessionUseCase(table_port=table_adapter)
list_survey_readings_use_case = ListSurveyReadingsUseCase(table_port=table_adapter)


def require_admin_access(authorization: str | None = Header(default=None)) -> str:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="admin authentication required")

    token = authorization.removeprefix("Bearer ").strip()
    if not token or not admin_auth.validate_token(token):
        raise HTTPException(status_code=401, detail="invalid admin token")
    return token
