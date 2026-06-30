from fastapi import APIRouter, Query

from app.api.schemas.analytics import APResponse, HeatmapResponse, IssuesResponse
from app.services.dependencies import (
    get_ap_summary_use_case,
    get_heatmap_use_case,
    get_issue_summary_use_case,
)


router = APIRouter()


@router.get("/heatmap", response_model=HeatmapResponse)
def get_heatmap(floor_id: str = Query(..., min_length=1)) -> HeatmapResponse:
    return get_heatmap_use_case.execute(floor_id=floor_id)


@router.get("/ap", response_model=APResponse)
def get_ap_summary(floor_id: str = Query(..., min_length=1)) -> APResponse:
    return get_ap_summary_use_case.execute(floor_id=floor_id)


@router.get("/issues", response_model=IssuesResponse)
def get_issue_summary(floor_id: str = Query(..., min_length=1)) -> IssuesResponse:
    return get_issue_summary_use_case.execute(floor_id=floor_id)
