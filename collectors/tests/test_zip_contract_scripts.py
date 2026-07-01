from pathlib import Path


REQUIRED_ARTIFACTS = [
    "metadata.json",
    "scan.json",
    "networks.txt",
    "interface.txt",
    "logs",
]

METADATA_FIELDS = [
    "schemaVersion",
    "platform",
    "collectedAt",
    "sessionId",
    "hostnameHash",
]

SCAN_READING_FIELDS = [
    "ssid",
    "bssid",
    "channel",
    "band",
    "signal_dbm",
    "captured_at",
]


def _read_script(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_windows_collector_mentions_required_contract_files() -> None:
    script = _read_script(Path("collectors/windows/collect.ps1"))
    for name in REQUIRED_ARTIFACTS:
        assert name in script


def test_macos_collector_mentions_required_contract_files() -> None:
    script = _read_script(Path("collectors/macos/collect.sh"))
    for name in REQUIRED_ARTIFACTS:
        assert name in script


def test_collectors_define_required_metadata_fields() -> None:
    windows = _read_script(Path("collectors/windows/collect.ps1"))
    macos = _read_script(Path("collectors/macos/collect.sh"))

    for field in METADATA_FIELDS:
        assert field in windows
        assert field in macos


def test_collectors_define_required_scan_reading_fields() -> None:
    windows = _read_script(Path("collectors/windows/collect.ps1"))
    macos = _read_script(Path("collectors/macos/collect.sh"))

    for field in SCAN_READING_FIELDS:
        assert field in windows
        assert field in macos


def test_collectors_use_hashed_host_identifier() -> None:
    windows = _read_script(Path("collectors/windows/collect.ps1"))
    macos = _read_script(Path("collectors/macos/collect.sh"))

    assert "SHA256" in windows
    assert "shasum -a 256" in macos


def test_windows_collector_uses_a_periodic_session_window() -> None:
    windows = _read_script(Path("collectors/windows/collect.ps1"))

    assert "UTF8Encoding" in windows
    assert "SessionDurationSeconds" in windows
    assert "SampleIntervalSeconds" in windows
    assert "WaveTracker Windows collector started" in windows
    assert "Collecting sample" in windows
    assert "Waiting" in windows
    assert "Get-NetworkReadings" in windows
    assert "netsh wlan show networks mode=bssid" in windows
    assert "Start-Sleep" in windows
    assert "while ((Get-Date) -lt $sessionEnd)" in windows


def test_macos_collector_uses_a_periodic_session_window() -> None:
    macos = _read_script(Path("collectors/macos/collect.sh"))

    assert 'LANG="en_US.UTF-8"' in macos
    assert 'LC_ALL="en_US.UTF-8"' in macos
    assert "SESSION_DURATION_SECONDS" in macos
    assert "SAMPLE_INTERVAL_SECONDS" in macos
    assert "WaveTracker macOS collector started" in macos
    assert "Collecting sample" in macos
    assert "Waiting" in macos
    assert 'while [ "$(date +%s)" -lt "${SESSION_END_SECONDS}" ]' in macos
    assert 'sleep "${SLEEP_SECONDS}"' in macos
