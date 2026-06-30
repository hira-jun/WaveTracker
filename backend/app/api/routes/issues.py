from fastapi import APIRouter, HTTPException, Query

from app.api.schemas.issues import IssueReport, IssueReportCreate
from app.services.dependencies import create_issue_use_case, list_issues_use_case
from app.services.use_cases.issues import FloorNotFoundError


router = APIRouter()


@router.post("", response_model=IssueReport)
def create_issue(payload: IssueReportCreate) -> IssueReport:
    try:
        return create_issue_use_case.execute(payload)
    except FloorNotFoundError as exc:
        raise HTTPException(status_code=404, detail="floor not found") from exc


@router.get("", response_model=list[IssueReport])
def list_issues(floor_id: str | None = Query(default=None)) -> list[IssueReport]:
    return list_issues_use_case.execute(floor_id=floor_id)
