from fastapi import APIRouter, Query

from app.api.schemas.analytics import APResponse, BandSummary, HeatmapPoint, HeatmapResponse, IssuesResponse
from app.domain.rssi_rules import classify_rssi
from app.domain.wifi_bands import WIFI_BANDS, normalize_band
from app.services.dependencies import table_adapter


router = APIRouter()


@router.get("/heatmap", response_model=HeatmapResponse)
def get_heatmap(floor_id: str = Query(..., min_length=1)) -> HeatmapResponse:
    readings = table_adapter.get_readings(floor_id=floor_id)
    points = [
        HeatmapPoint(
            x_norm=reading.x_norm,
            y_norm=reading.y_norm,
            signal_dbm=reading.signal_dbm,
            level=classify_rssi(reading.signal_dbm),
            band=normalize_band(reading.band, channel=reading.channel),
        )
        for reading in readings
    ]
    return HeatmapResponse(floor_id=floor_id, points=points)


@router.get("/ap", response_model=APResponse)
def get_ap_summary(floor_id: str = Query(..., min_length=1)) -> APResponse:
    readings = table_adapter.get_readings(floor_id=floor_id)
    by_band: dict[str, int] = {band: 0 for band in WIFI_BANDS}
    for reading in readings:
        band = normalize_band(reading.band, channel=reading.channel)
        by_band[band] += 1

    return APResponse(
        floor_id=floor_id,
        by_band=[BandSummary(band=band, count=by_band[band]) for band in WIFI_BANDS],
    )


@router.get("/issues", response_model=IssuesResponse)
def get_issue_summary(floor_id: str = Query(..., min_length=1)) -> IssuesResponse:
    return table_adapter.get_issue_summary(floor_id=floor_id)
