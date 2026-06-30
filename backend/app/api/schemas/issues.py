from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


IssueType = Literal["connection_unavailable", "latency", "disconnect", "auth_failure"]
IssueSeverity = Literal["low", "medium", "high"]


class IssueReportCreate(BaseModel):
    floor_id: str
    x_norm: float = Field(ge=0, le=1)
    y_norm: float = Field(ge=0, le=1)
    occurred_at: datetime
    ssid: str
    issue_type: IssueType
    severity: IssueSeverity


class IssueReport(IssueReportCreate):
    id: str
