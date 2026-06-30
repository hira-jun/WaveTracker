from typing import Literal

from pydantic import BaseModel


class HeatmapPoint(BaseModel):
    x_norm: float
    y_norm: float
    signal_dbm: int
    level: str
    band: Literal["2.4GHz", "5GHz", "6GHz"]


class HeatmapResponse(BaseModel):
    floor_id: str
    points: list[HeatmapPoint]


class BandSummary(BaseModel):
    band: Literal["2.4GHz", "5GHz", "6GHz"]
    count: int


class APResponse(BaseModel):
    floor_id: str
    by_band: list[BandSummary]


class IssuesResponse(BaseModel):
    floor_id: str
    issue_count: int
