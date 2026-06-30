from pydantic import BaseModel, Field


class FloorBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class FloorCreate(FloorBase):
    pass


class Floor(FloorBase):
    id: str
    map_image_url: str | None = None


class FloorMapUpload(BaseModel):
    map_image_url: str = Field(min_length=1)
