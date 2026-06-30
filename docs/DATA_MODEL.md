# Data Model

## Tables (Logical)

- `Floors`
- `SurveySessions`
- `SurveyReadings`
- `IssueReports`
- `AccessPoints` (planned)

## Floor

- `id: string`
- `name: string`
- `map_image_url?: string`

## SurveySession

- `id: string`
- `floor_id: string`
- `captured_at: datetime`
- `source_filename: string`
- `metadata: object`
- `networks_excerpt?: string`
- `interface_excerpt?: string`
- `log_files: string[]`

## SurveyReading

- `floor_id: string`
- `x_norm: number (0..1)`
- `y_norm: number (0..1)`
- `ssid: string`
- `bssid: string`
- `band: "2.4GHz" | "5GHz" | "6GHz"`
- `channel: int`
- `signal_dbm: int`
- `captured_at: datetime`

## IssueReport

- `id: string`
- `floor_id: string`
- `x_norm: number (0..1)`
- `y_norm: number (0..1)`
- `occurred_at: datetime`
- `ssid: string`
- `issue_type: connection_unavailable | latency | disconnect | auth_failure`
- `severity: low | medium | high`
