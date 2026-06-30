from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.schemas.floors import Floor, FloorCreate, FloorMapUpload
from app.services.dependencies import (
    create_floor_use_case,
    list_floors_use_case,
    require_admin_access,
    set_floor_map_use_case,
    upload_floor_map_use_case,
)
from app.services.use_cases.floors import FloorNotFoundError


router = APIRouter()


@router.get("", response_model=list[Floor])
def list_floors() -> list[Floor]:
    return list_floors_use_case.execute()


@router.post("", response_model=Floor)
def create_floor(
    payload: FloorCreate,
    _admin: None = Depends(require_admin_access),
) -> Floor:
    del _admin
    return create_floor_use_case.execute(name=payload.name)


@router.post("/{floor_id}/map", response_model=Floor)
def upload_floor_map(
    floor_id: str,
    payload: FloorMapUpload,
    _admin: None = Depends(require_admin_access),
) -> Floor:
    del _admin
    try:
        return set_floor_map_use_case.execute(floor_id=floor_id, map_image_url=payload.map_image_url)
    except FloorNotFoundError as exc:
        raise HTTPException(status_code=404, detail="floor not found") from exc


@router.post("/{floor_id}/map/upload", response_model=Floor)
async def upload_floor_map_file(
    floor_id: str,
    map_file: UploadFile = File(...),
    _admin: None = Depends(require_admin_access),
) -> Floor:
    del _admin
    payload = await map_file.read()
    try:
        return upload_floor_map_use_case.execute(
            floor_id=floor_id,
            filename=map_file.filename or "map.png",
            payload=payload,
        )
    except FloorNotFoundError as exc:
        raise HTTPException(status_code=404, detail="floor not found") from exc
