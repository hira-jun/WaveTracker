import json
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import pytest

from app.services.dependencies import admin_auth


@pytest.fixture
def zip_payload_builder():
    def _build(files: dict[str, object]) -> bytes:
        buffer = BytesIO()
        with ZipFile(buffer, "w") as archive:
            for path, content in files.items():
                if isinstance(content, str):
                    archive.writestr(path, content)
                else:
                    archive.writestr(path, json.dumps(content))
        return buffer.getvalue()

    return _build


@pytest.fixture
def reset_admin_state():
    def _reset() -> None:
        admin_auth._tokens = {}
        admin_auth._password_salt = ""
        admin_auth._password_hash = ""
        admin_auth._settings = {}
        state_path = Path(admin_auth._state_path)
        if state_path.exists():
            state_path.unlink()

    return _reset
