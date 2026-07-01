#!/usr/bin/env sh
set -eu

export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"

OUTPUT_DIR="${1:-./out}"
SESSION_DURATION_SECONDS="${2:-60}"
SAMPLE_INTERVAL_SECONDS="${3:-10}"

if [ "${SESSION_DURATION_SECONDS}" -le 0 ]; then
	echo "Session duration must be greater than zero." >&2
	exit 1
fi

if [ "${SAMPLE_INTERVAL_SECONDS}" -le 0 ]; then
	echo "Sample interval must be greater than zero." >&2
	exit 1
fi

SESSION_START_SECONDS="$(date +%s)"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
SESSION_END_SECONDS="$((SESSION_START_SECONDS + SESSION_DURATION_SECONDS))"
SESSION_DIR="${OUTPUT_DIR}/wifi-survey-${TIMESTAMP}"
LOGS_DIR="${SESSION_DIR}/logs"

mkdir -p "${SESSION_DIR}" "${LOGS_DIR}"

NETWORKS_TXT="${SESSION_DIR}/networks.txt"
INTERFACE_TXT="${SESSION_DIR}/interface.txt"
SCAN_JSON="${SESSION_DIR}/scan.json"
METADATA_JSON="${SESSION_DIR}/metadata.json"

WIFI_DEVICE="$(networksetup -listallhardwareports | awk '/Hardware Port: Wi-Fi|Hardware Port: AirPort/{getline; print $2; exit}')"

LATEST_NETWORKS_TEXT=""
LATEST_INTERFACE_TEXT=""
SCAN_JSON_FIRST_ENTRY=1

resolve_band_from_channel() {
	channel="$1"
	if [ "${channel}" -ge 1 ] && [ "${channel}" -le 14 ]; then
		echo "2.4GHz"
		return
	fi

	if [ "${channel}" -ge 181 ]; then
		echo "6GHz"
		return
	fi

	echo "5GHz"
}

echo "WaveTracker macOS collector started: sampling every ${SAMPLE_INTERVAL_SECONDS} seconds for about ${SESSION_DURATION_SECONDS} seconds"

cat > "${SCAN_JSON}" <<EOF
{
	"readings": [
EOF

SAMPLE_INDEX=0

while [ "$(date +%s)" -lt "${SESSION_END_SECONDS}" ]; do
	SAMPLE_INDEX=$((SAMPLE_INDEX + 1))
	CAPTURED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
	REMAINING_SECONDS="$((SESSION_END_SECONDS - $(date +%s)))"
	if [ "${REMAINING_SECONDS}" -lt 0 ]; then
		REMAINING_SECONDS=0
	fi
	echo "Collecting sample ${SAMPLE_INDEX} (about ${REMAINING_SECONDS} seconds remaining)"

	if [ -n "${WIFI_DEVICE}" ]; then
		LATEST_NETWORKS_TEXT="$(networksetup -getairportnetwork "${WIFI_DEVICE}" 2>/dev/null || true)"
		LATEST_INTERFACE_TEXT="$(ifconfig "${WIFI_DEVICE}" 2>/dev/null || true)"
	else
		LATEST_NETWORKS_TEXT="$(system_profiler SPAirPortDataType 2>/dev/null || true)"
		LATEST_INTERFACE_TEXT="$(system_profiler SPAirPortDataType 2>/dev/null || true)"
	fi

	printf '%s\n' "${LATEST_NETWORKS_TEXT}" > "${NETWORKS_TXT}"
	printf '%s\n' "${LATEST_INTERFACE_TEXT}" > "${INTERFACE_TXT}"
	system_profiler SPAirPortDataType > "${LOGS_DIR}/system_profiler.txt" 2>/dev/null || true

	AIRPORT_INFO="$(system_profiler SPAirPortDataType 2>/dev/null || true)"
	SSID="$(printf '%s\n' "${AIRPORT_INFO}" | awk -F': ' '/^[[:space:]]*SSID: / {print $2; exit}')"
	BSSID="$(printf '%s\n' "${AIRPORT_INFO}" | awk -F': ' '/^[[:space:]]*BSSID: / {print $2; exit}')"
	CHANNEL="$(printf '%s\n' "${AIRPORT_INFO}" | awk -F': ' '/^[[:space:]]*Channel: / {gsub(/[^0-9].*$/, "", $2); print $2; exit}')"
	RSSI="$(printf '%s\n' "${AIRPORT_INFO}" | awk -F': ' '/^[[:space:]]*RSSI: / {gsub(/[^0-9-].*$/, "", $2); print $2; exit}')"
	CHANNEL_VALUE="${CHANNEL:-0}"
	BAND="$(resolve_band_from_channel "${CHANNEL_VALUE}")"

	if [ ${SCAN_JSON_FIRST_ENTRY} -eq 1 ]; then
		SCAN_JSON_FIRST_ENTRY=0
	else
		printf ',\n' >> "${SCAN_JSON}"
	fi

	cat >> "${SCAN_JSON}" <<EOF
		{
			"ssid": "${SSID:-unknown-ssid}",
			"bssid": "${BSSID:-00:00:00:00:00:00}",
			"channel": ${CHANNEL_VALUE},
			"band": "${BAND}",
			"signal_dbm": ${RSSI:--90},
			"captured_at": "${CAPTURED_AT}"
		}
EOF

	NOW_SECONDS="$(date +%s)"
	NEXT_SAMPLE_SECONDS="$(( NOW_SECONDS + SAMPLE_INTERVAL_SECONDS ))"
	if [ "${NEXT_SAMPLE_SECONDS}" -ge "${SESSION_END_SECONDS}" ]; then
		break
	fi

	SLEEP_SECONDS="$(( NEXT_SAMPLE_SECONDS - $(date +%s) ))"
	if [ "${SLEEP_SECONDS}" -gt 0 ]; then
		echo "Waiting ${SLEEP_SECONDS} seconds before the next sample"
		sleep "${SLEEP_SECONDS}"
	fi
done

cat >> "${SCAN_JSON}" <<EOF

	]
}
EOF

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

ZIP_PATH="${OUTPUT_DIR}/wifi-survey-${TIMESTAMP}.zip"
rm -f "${ZIP_PATH}"

(
	cd "${SESSION_DIR}"
	zip -r "${ZIP_PATH}" . >/dev/null
)

echo "WaveTracker macOS collector completed: ${ZIP_PATH}"