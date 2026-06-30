from app.api.schemas.analytics import APResponse, BandSummary, HeatmapPoint, HeatmapResponse, IssuesResponse
from app.domain.rssi_rules import classify_rssi
from app.domain.wifi_bands import WIFI_BANDS, normalize_band
from app.services.storage.table_port import TablePort


class GetHeatmapUseCase:
    def __init__(self, *, table_port: TablePort) -> None:
        self._table_port = table_port

    def execute(self, *, floor_id: str) -> HeatmapResponse:
        readings = self._table_port.get_readings(floor_id=floor_id)
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


class GetAPSummaryUseCase:
    def __init__(self, *, table_port: TablePort) -> None:
        self._table_port = table_port

    def execute(self, *, floor_id: str) -> APResponse:
        readings = self._table_port.get_readings(floor_id=floor_id)
        by_band: dict[str, int] = {band: 0 for band in WIFI_BANDS}
        for reading in readings:
            band = normalize_band(reading.band, channel=reading.channel)
            by_band[band] += 1

        return APResponse(
            floor_id=floor_id,
            by_band=[BandSummary(band=band, count=by_band[band]) for band in WIFI_BANDS],
        )


class GetIssueSummaryUseCase:
    def __init__(self, *, table_port: TablePort) -> None:
        self._table_port = table_port

    def execute(self, *, floor_id: str) -> IssuesResponse:
        return self._table_port.get_issue_summary(floor_id=floor_id)
