from app.api.schemas.issues import IssueReport, IssueReportCreate
from app.services.storage.table_port import TablePort


class FloorNotFoundError(ValueError):
    pass


class CreateIssueUseCase:
    def __init__(self, *, table_port: TablePort) -> None:
        self._table_port = table_port

    def execute(self, payload: IssueReportCreate) -> IssueReport:
        if payload.floor_id not in {floor.id for floor in self._table_port.list_floors()}:
            raise FloorNotFoundError("floor not found")
        return self._table_port.create_issue_report(payload)


class ListIssuesUseCase:
    def __init__(self, *, table_port: TablePort) -> None:
        self._table_port = table_port

    def execute(self, *, floor_id: str | None = None) -> list[IssueReport]:
        return self._table_port.list_issue_reports(floor_id=floor_id)
