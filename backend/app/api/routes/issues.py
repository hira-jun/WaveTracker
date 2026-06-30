from fastapi import APIRouter, HTTPException, Query

from app.api.schemas.issues import IssueReport, IssueReportCreate
from app.services.dependencies import table_adapter


router = APIRouter()


@router.post("", response_model=IssueReport)
def create_issue(payload: IssueReportCreate) -> IssueReport:
    if payload.floor_id not in {floor.id for floor in table_adapter.list_floors()}:
        raise HTTPException(status_code=404, detail="floor not found")
    return table_adapter.create_issue_report(payload)


@router.get("", response_model=list[IssueReport])
def list_issues(floor_id: str | None = Query(default=None)) -> list[IssueReport]:
    return table_adapter.list_issue_reports(floor_id=floor_id)
