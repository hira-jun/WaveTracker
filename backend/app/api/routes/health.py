from fastapi import APIRouter

from app.api.schemas.health import HealthResponse
from app.services.system_status import get_system_status


router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    status = get_system_status()
    return HealthResponse(status=status)
