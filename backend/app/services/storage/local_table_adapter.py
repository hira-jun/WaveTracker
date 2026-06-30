from datetime import UTC, datetime
from uuid import uuid4

from app.api.schemas.analytics import IssuesResponse
from app.api.schemas.floors import Floor
from app.api.schemas.issues import IssueReport, IssueReportCreate
from app.api.schemas.survey import SurveyReading, SurveySession


class LocalTableAdapter:
    def __init__(self) -> None:
        self._floors: dict[str, Floor] = {}
        self._sessions: dict[str, SurveySession] = {}
        self._readings: list[SurveyReading] = []
        self._issues: list[IssueReport] = []

    def list_floors(self) -> list[Floor]:
        return list(self._floors.values())

    def create_floor(self, name: str) -> Floor:
        floor = Floor(id=f"floor-{uuid4()}", name=name)
        self._floors[floor.id] = floor
        return floor

    def set_floor_map(self, floor_id: str, map_image_url: str) -> Floor:
        floor = self._floors[floor_id]
        updated = floor.model_copy(update={"map_image_url": map_image_url})
        self._floors[floor_id] = updated
        return updated

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
        session = SurveySession(
            id=f"session-{uuid4()}",
            floor_id=floor_id,
            source_filename=source_filename,
            captured_at=datetime.now(UTC),
            location_x_norm=location_x_norm,
            location_y_norm=location_y_norm,
            metadata=metadata or {},
            networks_excerpt=networks_excerpt,
            interface_excerpt=interface_excerpt,
            log_files=log_files or [],
        )
        self._sessions[session.id] = session
        return session

    def add_readings(self, readings: list[SurveyReading]) -> None:
        self._readings.extend(readings)

    def list_survey_sessions(self, floor_id: str | None = None) -> list[SurveySession]:
        sessions = list(self._sessions.values())
        if floor_id is None:
            return sessions
        return [session for session in sessions if session.floor_id == floor_id]

    def get_survey_session(self, session_id: str) -> SurveySession | None:
        return self._sessions.get(session_id)

    def get_readings(self, floor_id: str | None = None) -> list[SurveyReading]:
        if floor_id is None:
            return list(self._readings)
        return [reading for reading in self._readings if reading.floor_id == floor_id]

    def create_issue_report(self, payload: IssueReportCreate) -> IssueReport:
        issue = IssueReport(id=f"issue-{uuid4()}", **payload.model_dump())
        self._issues.append(issue)
        return issue

    def list_issue_reports(self, floor_id: str | None = None) -> list[IssueReport]:
        if floor_id is None:
            return list(self._issues)
        return [issue for issue in self._issues if issue.floor_id == floor_id]

    def get_issue_summary(self, floor_id: str) -> IssuesResponse:
        return IssuesResponse(
            floor_id=floor_id,
            issue_count=len(self.list_issue_reports(floor_id=floor_id)),
        )
