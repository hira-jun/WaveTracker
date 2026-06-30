from app.api.schemas.floors import Floor
from app.services.storage.blob_port import BlobPort
from app.services.storage.table_port import TablePort


class FloorNotFoundError(ValueError):
    pass


class ListFloorsUseCase:
    def __init__(self, *, table_port: TablePort) -> None:
        self._table_port = table_port

    def execute(self) -> list[Floor]:
        return self._table_port.list_floors()


class CreateFloorUseCase:
    def __init__(self, *, table_port: TablePort) -> None:
        self._table_port = table_port

    def execute(self, *, name: str) -> Floor:
        return self._table_port.create_floor(name=name)


class SetFloorMapUseCase:
    def __init__(self, *, table_port: TablePort) -> None:
        self._table_port = table_port

    def execute(self, *, floor_id: str, map_image_url: str) -> Floor:
        try:
            return self._table_port.set_floor_map(floor_id=floor_id, map_image_url=map_image_url)
        except KeyError as exc:
            raise FloorNotFoundError("floor not found") from exc


class UploadFloorMapUseCase:
    def __init__(self, *, table_port: TablePort, blob_port: BlobPort) -> None:
        self._table_port = table_port
        self._blob_port = blob_port

    def execute(self, *, floor_id: str, filename: str, payload: bytes) -> Floor:
        if floor_id not in {floor.id for floor in self._table_port.list_floors()}:
            raise FloorNotFoundError("floor not found")

        saved_path = self._blob_port.save_floor_map(
            floor_id=floor_id,
            filename=filename,
            payload=payload,
        )
        return self._table_port.set_floor_map(floor_id=floor_id, map_image_url=str(saved_path))
