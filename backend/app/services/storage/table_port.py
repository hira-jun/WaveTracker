from typing import Protocol

from app.api.schemas.analytics import IssuesResponse
from app.api.schemas.floors import Floor
from app.api.schemas.issues import IssueReport, IssueReportCreate
from app.api.schemas.survey import SurveyReading, SurveySession


class TablePort(Protocol):
    def list_floors(self) -> list[Floor]:
        ...

    def create_floor(self, name: str) -> Floor:
        ...

    def set_floor_map(self, floor_id: str, map_image_url: str) -> Floor:
        ...

    def add_survey_session(
        self,
        floor_id: str,
        source_filename: str,
        location_x_norm: float | None = None,
        location_y_norm: float | None = None,
        metadata: dict | None = None,
        networks_excerpt: str | None = None,
        interface_excerpt: str | None = None,
        log_files: list[str] | None = None,
    ) -> SurveySession:
        ...

    def add_readings(self, readings: list[SurveyReading]) -> None:
        ...

    def list_survey_sessions(self, floor_id: str | None = None) -> list[SurveySession]:
        ...

    def get_survey_session(self, session_id: str) -> SurveySession | None:
        ...

    def get_readings(self, floor_id: str | None = None) -> list[SurveyReading]:
        ...

    def create_issue_report(self, payload: IssueReportCreate) -> IssueReport:
        ...

    def list_issue_reports(self, floor_id: str | None = None) -> list[IssueReport]:
        ...

    def get_issue_summary(self, floor_id: str) -> IssuesResponse:
        ...
