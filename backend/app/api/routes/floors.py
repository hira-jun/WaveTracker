from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.schemas.floors import Floor, FloorCreate, FloorMapUpload
from app.services.dependencies import blob_adapter, require_admin_access, table_adapter


router = APIRouter()


@router.get("", response_model=list[Floor])
def list_floors() -> list[Floor]:
    return table_adapter.list_floors()


@router.post("", response_model=Floor)
def create_floor(
    payload: FloorCreate,
    _admin: None = Depends(require_admin_access),
) -> Floor:
    del _admin
    return table_adapter.create_floor(name=payload.name)


@router.post("/{floor_id}/map", response_model=Floor)
def upload_floor_map(
    floor_id: str,
    payload: FloorMapUpload,
    _admin: None = Depends(require_admin_access),
) -> Floor:
    del _admin
    try:
        return table_adapter.set_floor_map(floor_id=floor_id, map_image_url=payload.map_image_url)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="floor not found") from exc


@router.post("/{floor_id}/map/upload", response_model=Floor)
async def upload_floor_map_file(
    floor_id: str,
    map_file: UploadFile = File(...),
    _admin: None = Depends(require_admin_access),
) -> Floor:
    del _admin
    if floor_id not in {floor.id for floor in table_adapter.list_floors()}:
        raise HTTPException(status_code=404, detail="floor not found")

    payload = await map_file.read()
    saved_path = blob_adapter.save_floor_map(
        floor_id=floor_id,
        filename=map_file.filename or "map.png",
        payload=payload,
    )
    return table_adapter.set_floor_map(floor_id=floor_id, map_image_url=str(saved_path))
