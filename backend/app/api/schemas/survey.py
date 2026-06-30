from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class SurveyReading(BaseModel):
    floor_id: str
    x_norm: float = Field(ge=0, le=1)
    y_norm: float = Field(ge=0, le=1)
    ssid: str
    bssid: str
    band: Literal["2.4GHz", "5GHz", "6GHz"]
    channel: int
    signal_dbm: int
    captured_at: datetime


class SurveySession(BaseModel):
    id: str
    floor_id: str
    captured_at: datetime
    source_filename: str
    location_x_norm: float | None = Field(default=None, ge=0, le=1)
    location_y_norm: float | None = Field(default=None, ge=0, le=1)
    metadata: dict = Field(default_factory=dict)
    networks_excerpt: str | None = None
    interface_excerpt: str | None = None
    log_files: list[str] = Field(default_factory=list)


class SurveyUploadResponse(BaseModel):
    session: SurveySession
    reading_count: int
