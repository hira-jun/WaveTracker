from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas.admin import (
    AdminLoginRequest,
    AdminLoginResponse,
    AdminLogoutResponse,
    AdminPasswordChangeRequest,
    AdminPasswordChangeResponse,
    AdminSettingsResponse,
    AdminSettingsUpdate,
    AdminSetupRequest,
    AdminStatusResponse,
)
from app.services.dependencies import admin_auth, require_admin_access


router = APIRouter()


@router.get("/status", response_model=AdminStatusResponse)
def get_admin_status() -> AdminStatusResponse:
    return AdminStatusResponse(initialized=admin_auth.is_initialized())


@router.post("/setup", response_model=AdminStatusResponse)
def setup_admin_password(payload: AdminSetupRequest) -> AdminStatusResponse:
    try:
        admin_auth.setup_password(payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return AdminStatusResponse(initialized=True)


@router.post("/login", response_model=AdminLoginResponse)
def login_admin(payload: AdminLoginRequest) -> AdminLoginResponse:
    if not admin_auth.verify_password(payload.password):
        raise HTTPException(status_code=401, detail="invalid password")
    return AdminLoginResponse(token=admin_auth.issue_token())


@router.get("/settings", response_model=AdminSettingsResponse)
def get_admin_settings(_admin_token: str = Depends(require_admin_access)) -> AdminSettingsResponse:
    del _admin_token
    return AdminSettingsResponse(settings=admin_auth.get_settings())


@router.put("/settings", response_model=AdminSettingsResponse)
def update_admin_settings(
    payload: AdminSettingsUpdate,
    _admin_token: str = Depends(require_admin_access),
) -> AdminSettingsResponse:
    del _admin_token
    return AdminSettingsResponse(settings=admin_auth.update_settings(payload))


@router.post("/logout", response_model=AdminLogoutResponse)
def logout_admin(admin_token: str = Depends(require_admin_access)) -> AdminLogoutResponse:
    admin_auth.revoke_token(admin_token)
    return AdminLogoutResponse(logged_out=True)


@router.post("/change-password", response_model=AdminPasswordChangeResponse)
def change_admin_password(
    payload: AdminPasswordChangeRequest,
    _admin_token: str = Depends(require_admin_access),
) -> AdminPasswordChangeResponse:
    del _admin_token
    try:
        admin_auth.change_password(
            current_password=payload.current_password,
            new_password=payload.new_password,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return AdminPasswordChangeResponse(changed=True)