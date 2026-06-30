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
- Commands used:
  - `netsh wlan show networks mode=bssid`
  - `netsh wlan show interfaces`
  - `netsh wlan show wlanreport`
- Collector output is built from built-in PowerShell and netsh only.

## macOS

- Script: `collectors/macos/collect.sh`
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
- macOS example:
  - `sh collectors/macos/collect.sh ./out`
