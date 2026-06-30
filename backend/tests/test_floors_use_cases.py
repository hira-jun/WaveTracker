import pytest

from app.services.storage.local_blob_adapter import LocalBlobAdapter
from app.services.storage.local_table_adapter import LocalTableAdapter
from app.services.use_cases.floors import (
    CreateFloorUseCase,
    FloorNotFoundError,
    ListFloorsUseCase,
    SetFloorMapUseCase,
    UploadFloorMapUseCase,
)


def test_list_and_create_floor_use_cases() -> None:
    table = LocalTableAdapter()
    create_use_case = CreateFloorUseCase(table_port=table)
    list_use_case = ListFloorsUseCase(table_port=table)

    created = create_use_case.execute(name="Lab")
    listed = list_use_case.execute()

    assert created.name == "Lab"
    assert any(item.id == created.id for item in listed)


def test_set_floor_map_raises_when_floor_missing() -> None:
    table = LocalTableAdapter()
    use_case = SetFloorMapUseCase(table_port=table)

    with pytest.raises(FloorNotFoundError):
        use_case.execute(floor_id="missing", map_image_url="map.png")


def test_upload_floor_map_persists_blob_and_updates_floor(tmp_path) -> None:
    table = LocalTableAdapter()
    blob = LocalBlobAdapter(base_dir=tmp_path)
    floor = table.create_floor("F1")
    use_case = UploadFloorMapUseCase(table_port=table, blob_port=blob)

    updated = use_case.execute(floor_id=floor.id, filename="map.png", payload=b"png-bytes")

    assert updated.map_image_url is not None
    assert floor.id in updated.map_image_url
    assert (tmp_path / "maps" / floor.id / "map.png").exists()
