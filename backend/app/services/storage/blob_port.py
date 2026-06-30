from pathlib import Path
from typing import Protocol


class BlobPort(Protocol):
    def save_raw_upload(self, filename: str, payload: bytes) -> Path:
        ...

    def save_floor_map(self, floor_id: str, filename: str, payload: bytes) -> Path:
        ...
