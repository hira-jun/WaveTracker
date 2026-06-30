import hashlib
import hmac
import json
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

from app.api.schemas.admin import AdminSettings, AdminSettingsUpdate


class AdminAuthService:
    def __init__(self) -> None:
        backend_root = Path(__file__).resolve().parents[2]
        self._state_path = backend_root / "data" / "admin" / "state.json"
        self._tokens: dict[str, datetime] = {}
        self._password_salt = ""
        self._password_hash = ""
        self._settings: dict[str, str | None] = {}
        self._load_state()

    def is_initialized(self) -> bool:
        return bool(self._password_salt and self._password_hash)

    def setup_password(self, password: str) -> None:
        if self.is_initialized():
            raise ValueError("admin password is already initialized")

        salt = os.urandom(16).hex()
        password_hash = self._hash_password(password=password, salt=salt)
        self._password_salt = salt
        self._password_hash = password_hash
        self._save_state()

    def verify_password(self, password: str) -> bool:
        if not self.is_initialized():
            return False

        expected = self._hash_password(password=password, salt=self._password_salt)
        return hmac.compare_digest(expected, self._password_hash)

    def issue_token(self) -> str:
        self._prune_tokens()
        token = uuid4().hex
        self._tokens[token] = datetime.now(UTC) + timedelta(hours=12)
        return token

    def validate_token(self, token: str) -> bool:
        self._prune_tokens()
        expires_at = self._tokens.get(token)
        return expires_at is not None and expires_at > datetime.now(UTC)

    def revoke_token(self, token: str) -> None:
        self._tokens.pop(token, None)

    def change_password(self, current_password: str, new_password: str) -> None:
        if not self.verify_password(current_password):
            raise ValueError("current password is invalid")

        salt = os.urandom(16).hex()
        password_hash = self._hash_password(password=new_password, salt=salt)
        self._password_salt = salt
        self._password_hash = password_hash
        self._tokens = {}
        self._save_state()

    def get_settings(self) -> AdminSettings:
        merged = {
            "dashboard_title": "WaveTracker",
            "default_floor_id": None,
            "maintenance_message": None,
        }
        merged.update(self._settings)
        return AdminSettings.model_validate(merged)

    def update_settings(self, payload: AdminSettingsUpdate) -> AdminSettings:
        updated = self.get_settings().model_dump()
        changes = payload.model_dump(exclude_unset=True)
        updated.update(changes)
        self._settings = {
            "dashboard_title": updated.get("dashboard_title"),
            "default_floor_id": updated.get("default_floor_id"),
            "maintenance_message": updated.get("maintenance_message"),
        }
        self._save_state()
        return self.get_settings()

    def _hash_password(self, password: str, salt: str) -> str:
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            200_000,
        )
        return digest.hex()

    def _load_state(self) -> None:
        if not self._state_path.exists():
            return

        with self._state_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        self._password_salt = str(data.get("password_salt", ""))
        self._password_hash = str(data.get("password_hash", ""))
        settings = data.get("settings", {})
        if isinstance(settings, dict):
            self._settings = {
                "dashboard_title": settings.get("dashboard_title"),
                "default_floor_id": settings.get("default_floor_id"),
                "maintenance_message": settings.get("maintenance_message"),
            }

    def _save_state(self) -> None:
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "password_salt": self._password_salt,
            "password_hash": self._password_hash,
            "settings": self._settings,
        }
        with self._state_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

    def _prune_tokens(self) -> None:
        now = datetime.now(UTC)
        expired_tokens = [token for token, expires_at in self._tokens.items() if expires_at <= now]
        for token in expired_tokens:
            self._tokens.pop(token, None)