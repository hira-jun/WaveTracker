# API Specification

## Health

- `GET /health`

Returns service health status.

## Floors

- `GET /floors`
- `POST /floors`
- `POST /floors/{floor_id}/map`
- `POST /floors/{floor_id}/map/upload`

Purpose:

- Floor master registration and map assignment.

## Survey

- `POST /survey/upload?floor_id=<id>&x_norm=<0..1>&y_norm=<0..1>`
- `GET /survey/readings?floor_id=<id>`
- `GET /survey/sessions?floor_id=<id>`
- `GET /survey/sessions/{session_id}`

Purpose:

- Upload collector ZIP, persist parsed readings, and attach the chosen floor-map location.
- Provide reading/session retrieval for UI.

## Issues

- `POST /issues`
- `GET /issues?floor_id=<id>`

Purpose:

- Register connection issues with location and severity.

## Analytics

- `GET /analytics/heatmap?floor_id=<id>`
- `GET /analytics/ap?floor_id=<id>`
- `GET /analytics/issues?floor_id=<id>`

Purpose:

- Heatmap points with RSSI level and normalized Wi-Fi band.
- AP band summary in fixed bands: 2.4GHz, 5GHz, 6GHz.
- Issue count summary by floor.
