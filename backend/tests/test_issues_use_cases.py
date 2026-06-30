from datetime import UTC, datetime

import pytest

from app.api.schemas.issues import IssueReportCreate
from app.services.storage.local_table_adapter import LocalTableAdapter
from app.services.use_cases.issues import CreateIssueUseCase, FloorNotFoundError, ListIssuesUseCase


def test_create_issue_requires_existing_floor() -> None:
    table = LocalTableAdapter()
    create_use_case = CreateIssueUseCase(table_port=table)

    payload = IssueReportCreate(
        floor_id="missing",
        x_norm=0.2,
        y_norm=0.3,
        occurred_at=datetime.now(UTC),
        ssid="ssid",
        issue_type="latency",
        severity="medium",
    )

    with pytest.raises(FloorNotFoundError):
        create_use_case.execute(payload)


def test_create_and_list_issues_by_floor() -> None:
    table = LocalTableAdapter()
    floor = table.create_floor("F2")
    create_use_case = CreateIssueUseCase(table_port=table)
    list_use_case = ListIssuesUseCase(table_port=table)

    payload = IssueReportCreate(
        floor_id=floor.id,
        x_norm=0.2,
        y_norm=0.3,
        occurred_at=datetime.now(UTC),
        ssid="ssid",
        issue_type="latency",
        severity="medium",
    )
    created = create_use_case.execute(payload)

    listed = list_use_case.execute(floor_id=floor.id)

    assert created.floor_id == floor.id
    assert len(listed) == 1
    assert listed[0].id == created.id
