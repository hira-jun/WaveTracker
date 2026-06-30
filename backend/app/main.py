import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.admin import router as admin_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.floors import router as floors_router
from app.api.routes.health import router as health_router
from app.api.routes.issues import router as issues_router
from app.api.routes.survey import router as survey_router


def _get_cors_origins() -> list[str]:
    configured = os.getenv("CORS_ALLOW_ORIGINS", "")
    if configured.strip():
        return [origin.strip() for origin in configured.split(",") if origin.strip()]
    return ["http://localhost:3000", "http://127.0.0.1:3000"]


app = FastAPI(title="WaveTracker API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_router)
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(floors_router, prefix="/floors", tags=["floors"])
app.include_router(survey_router, prefix="/survey", tags=["survey"])
app.include_router(issues_router, prefix="/issues", tags=["issues"])
app.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
