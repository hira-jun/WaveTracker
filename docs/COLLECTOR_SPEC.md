# Collector Specification

## Output Contract

Collector scripts generate `wifi-survey-<timestamp>.zip` with the following content:

- `metadata.json`
- `scan.json`
- `networks.txt`
- `interface.txt`
- `logs/` (one or more files)

## Privacy Rules

- Do not store personal identifiers directly.
- Store hashed hostname in `metadata.json`.
- Keep SSID/BSSID and radio diagnostics only.

## Windows

- Script: `collectors/windows/collect.ps1`
- Collector runs as a single session for about 1 minute and captures a scan every 10 seconds.
- One run produces one ZIP with multiple time-stamped readings in `scan.json`, and those readings are derived from the `networks.txt` network list rather than the interface summary.
- Collector writes text artifacts using UTF-8 and configures PowerShell output decoding for UTF-8 before calling `netsh`.
- Commands used:
  - `netsh wlan show networks mode=bssid`
  - `netsh wlan show interfaces`
  - `netsh wlan show wlanreport`
- Collector output is built from built-in PowerShell and netsh only.

## macOS

- Script: `collectors/macos/collect.sh`
- Collector runs as a single session for about 1 minute and captures a scan every 10 seconds.
- One run produces one ZIP with multiple time-stamped readings in `scan.json`.
- Collector forces `LANG` and `LC_ALL` to `en_US.UTF-8` so shell output stays in UTF-8.
- Commands used:
  - `networksetup -listallhardwareports`
  - `networksetup -getairportnetwork`
  - `ifconfig`
  - `system_profiler SPAirPortDataType`
- Collector output uses only built-in macOS tools and does not depend on the private airport binary.

## Manual Upload

- The web app requires a floor selection and a floor-map point before uploading a survey ZIP.
- The chosen `x_norm` / `y_norm` location is attached at upload time and used as the fallback location for readings that do not include coordinates in `scan.json`.

## Execution

- Windows example:
  - `pwsh -File collectors/windows/collect.ps1 -OutputDir .\\out`
- Windows session timing can be overridden with `-SessionDurationSeconds` and `-SampleIntervalSeconds` if needed.
- macOS example:
  - `sh collectors/macos/collect.sh ./out`
- macOS session timing can be overridden with positional arguments for duration and interval.
