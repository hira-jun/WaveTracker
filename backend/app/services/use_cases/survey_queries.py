from app.api.schemas.survey import SurveyReading, SurveySession
from app.services.storage.table_port import TablePort


class SurveySessionNotFoundError(ValueError):
    pass


class ListSurveySessionsUseCase:
    def __init__(self, *, table_port: TablePort) -> None:
        self._table_port = table_port

    def execute(self, floor_id: str | None = None) -> list[SurveySession]:
        return self._table_port.list_survey_sessions(floor_id=floor_id)


class GetSurveySessionUseCase:
    def __init__(self, *, table_port: TablePort) -> None:
        self._table_port = table_port

    def execute(self, session_id: str) -> SurveySession:
        session = self._table_port.get_survey_session(session_id)
        if session is None:
            raise SurveySessionNotFoundError("session not found")
        return session


class ListSurveyReadingsUseCase:
    def __init__(self, *, table_port: TablePort) -> None:
        self._table_port = table_port

    def execute(self, floor_id: str | None = None) -> list[SurveyReading]:
        return self._table_port.get_readings(floor_id=floor_id)
