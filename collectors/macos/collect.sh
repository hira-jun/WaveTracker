#!/usr/bin/env sh
set -eu

OUTPUT_DIR="${1:-./out}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
SESSION_DIR="${OUTPUT_DIR}/wifi-survey-${TIMESTAMP}"
LOGS_DIR="${SESSION_DIR}/logs"

mkdir -p "${SESSION_DIR}" "${LOGS_DIR}"

NETWORKS_TXT="${SESSION_DIR}/networks.txt"
INTERFACE_TXT="${SESSION_DIR}/interface.txt"
SCAN_JSON="${SESSION_DIR}/scan.json"
METADATA_JSON="${SESSION_DIR}/metadata.json"

WIFI_DEVICE="$(networksetup -listallhardwareports | awk '/Hardware Port: Wi-Fi|Hardware Port: AirPort/{getline; print $2; exit}')"

if [ -n "${WIFI_DEVICE}" ]; then
	networksetup -getairportnetwork "${WIFI_DEVICE}" > "${NETWORKS_TXT}" 2>/dev/null || true
	ifconfig "${WIFI_DEVICE}" > "${INTERFACE_TXT}" 2>/dev/null || true
else
	system_profiler SPAirPortDataType > "${NETWORKS_TXT}" 2>/dev/null || true
	system_profiler SPAirPortDataType > "${INTERFACE_TXT}" 2>/dev/null || true
fi

system_profiler SPAirPortDataType > "${LOGS_DIR}/system_profiler.txt"

AIRPORT_INFO="$(system_profiler SPAirPortDataType 2>/dev/null || true)"
SSID="$(printf '%s\n' "${AIRPORT_INFO}" | awk -F': ' '/^[[:space:]]*SSID: / {print $2; exit}')"
BSSID="$(printf '%s\n' "${AIRPORT_INFO}" | awk -F': ' '/^[[:space:]]*BSSID: / {print $2; exit}')"
CHANNEL="$(printf '%s\n' "${AIRPORT_INFO}" | awk -F': ' '/^[[:space:]]*Channel: / {gsub(/[^0-9].*$/, "", $2); print $2; exit}')"
RSSI="$(printf '%s\n' "${AIRPORT_INFO}" | awk -F': ' '/^[[:space:]]*RSSI: / {gsub(/[^0-9-].*$/, "", $2); print $2; exit}')"

HOSTNAME_HASH="$(hostname | shasum -a 256 | awk '{print $1}')"

cat > "${METADATA_JSON}" <<EOF
{
	"schemaVersion": "1.0",
	"platform": "macos",
	"collectedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
	"sessionId": "${TIMESTAMP}",
	"hostnameHash": "${HOSTNAME_HASH}"
}
EOF

cat > "${SCAN_JSON}" <<EOF
{
	"readings": [
		{
			"ssid": "${SSID:-unknown-ssid}",
			"bssid": "${BSSID:-00:00:00:00:00:00}",
			"channel": ${CHANNEL:-0},
			"signal_dbm": ${RSSI:--90},
			"captured_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
		}
	]
}
EOF

ZIP_PATH="${OUTPUT_DIR}/wifi-survey-${TIMESTAMP}.zip"
rm -f "${ZIP_PATH}"

(
	cd "${SESSION_DIR}"
	zip -r "${ZIP_PATH}" . >/dev/null
)

echo "WaveTracker macOS collector completed: ${ZIP_PATH}"