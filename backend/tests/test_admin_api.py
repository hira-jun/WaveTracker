from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.services.dependencies import admin_auth


def _reset_admin_state() -> None:
    admin_auth._tokens = {}
    admin_auth._password_salt = ""
    admin_auth._password_hash = ""
    admin_auth._settings = {}
    state_path = Path(admin_auth._state_path)
    if state_path.exists():
        state_path.unlink()


def test_admin_setup_and_login_flow() -> None:
    _reset_admin_state()
    client = TestClient(app)

    status_response = client.get("/admin/status")
    assert status_response.status_code == 200
    assert status_response.json()["initialized"] is False

    setup_response = client.post("/admin/setup", json={"password": "AdminPassw0rd!"})
    assert setup_response.status_code == 200
    assert setup_response.json()["initialized"] is True

    duplicate_setup_response = client.post("/admin/setup", json={"password": "AnotherPassw0rd!"})
    assert duplicate_setup_response.status_code == 409

    bad_login_response = client.post("/admin/login", json={"password": "wrong-pass"})
    assert bad_login_response.status_code == 401

    login_response = client.post("/admin/login", json={"password": "AdminPassw0rd!"})
    assert login_response.status_code == 200
    token = login_response.json()["token"]
    assert len(token) > 10

    settings_response = client.get(
        "/admin/settings",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert settings_response.status_code == 200
    assert settings_response.json()["settings"]["dashboard_title"] == "WaveTracker"


def test_floor_mutation_requires_admin_token() -> None:
    client = TestClient(app)

    create_response = client.post("/floors", json={"name": "Protected Floor"})
    assert create_response.status_code == 401


def test_admin_logout_revokes_token() -> None:
    _reset_admin_state()
    client = TestClient(app)

    setup_response = client.post("/admin/setup", json={"password": "AdminPassw0rd!"})
    assert setup_response.status_code == 200
    login_response = client.post("/admin/login", json={"password": "AdminPassw0rd!"})
    token = login_response.json()["token"]

    logout_response = client.post(
        "/admin/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert logout_response.status_code == 200
    assert logout_response.json()["logged_out"] is True

    settings_response = client.get(
        "/admin/settings",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert settings_response.status_code == 401


def test_admin_change_password_invalidates_existing_sessions() -> None:
    _reset_admin_state()
    client = TestClient(app)

    setup_response = client.post("/admin/setup", json={"password": "AdminPassw0rd!"})
    assert setup_response.status_code == 200
    login_response = client.post("/admin/login", json={"password": "AdminPassw0rd!"})
    token = login_response.json()["token"]

    change_response = client.post(
        "/admin/change-password",
        json={
            "current_password": "AdminPassw0rd!",
            "new_password": "NewAdminPassw0rd!",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert change_response.status_code == 200
    assert change_response.json()["changed"] is True

    old_password_login = client.post("/admin/login", json={"password": "AdminPassw0rd!"})
    assert old_password_login.status_code == 401

    new_password_login = client.post("/admin/login", json={"password": "NewAdminPassw0rd!"})
    assert new_password_login.status_code == 200