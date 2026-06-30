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


def test_collectors_use_hashed_host_identifier() -> None:
    windows = _read_script(Path("collectors/windows/collect.ps1"))
    macos = _read_script(Path("collectors/macos/collect.sh"))

    assert "SHA256" in windows
    assert "shasum -a 256" in macos
