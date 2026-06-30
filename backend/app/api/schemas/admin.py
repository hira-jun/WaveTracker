from pydantic import BaseModel, Field


class AdminStatusResponse(BaseModel):
    initialized: bool


class AdminSetupRequest(BaseModel):
    password: str = Field(min_length=8, max_length=128)


class AdminLoginRequest(BaseModel):
    password: str = Field(min_length=1, max_length=128)


class AdminLoginResponse(BaseModel):
    token: str


class AdminLogoutResponse(BaseModel):
    logged_out: bool


class AdminPasswordChangeRequest(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class AdminPasswordChangeResponse(BaseModel):
    changed: bool


class AdminSettings(BaseModel):
    dashboard_title: str = Field(default="WaveTracker", min_length=1, max_length=100)
    default_floor_id: str | None = Field(default=None, max_length=100)
    maintenance_message: str | None = Field(default=None, max_length=300)


class AdminSettingsUpdate(BaseModel):
    dashboard_title: str | None = Field(default=None, min_length=1, max_length=100)
    default_floor_id: str | None = Field(default=None, max_length=100)
    maintenance_message: str | None = Field(default=None, max_length=300)


class AdminSettingsResponse(BaseModel):
    settings: AdminSettings