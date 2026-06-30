from pathlib import Path


class LocalBlobAdapter:
    def __init__(self, base_dir: Path | None = None) -> None:
        self._base_dir = base_dir or Path("data/raw")
        self._base_dir.mkdir(parents=True, exist_ok=True)

    def save_raw_upload(self, filename: str, payload: bytes) -> Path:
        target = self._base_dir / filename
        target.write_bytes(payload)
        return target

    def save_floor_map(self, floor_id: str, filename: str, payload: bytes) -> Path:
        maps_dir = self._base_dir / "maps" / floor_id
        maps_dir.mkdir(parents=True, exist_ok=True)
        safe_name = filename or "map.png"
        target = maps_dir / safe_name
        target.write_bytes(payload)
        return target
