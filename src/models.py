from datetime import datetime
from typing import List, Optional, Tuple

from geojson_pydantic import Feature
from pydantic import (
    BaseModel,
    Field,
    PydanticValueError,
    root_validator,
    validator,
)


class DataModel(BaseModel):
    ids: Optional[str] = None

    bbox: Optional[Tuple[float, float, float, float]]
    contains: Optional[Feature]
    intersects: Optional[Feature]

    limit: Optional[int] = Field(1, ge=1, le=500)

    zoom_level: Optional[int] = Field(18, ge=10, le=18)

    time_series: Optional[List[Tuple[str, str]]]
    time: str

    max_cloud_cover: Optional[int] = Field(100, ge=0, le=100)

    @validator("bbox")
    def bbox_in_WGS84_bounds(cls, bbox):
        if not all(
            [
                bbox[0] >= -180,
                bbox[1] >= -90,
                bbox[2] <= 180,
                bbox[3] <= 90,
            ]
        ):
            raise PydanticValueError("Bbox not in WGS84 bounds [±180; ±90]")

    @validator("time")
    def validate_time(cls, time: str):
        begin, end = time.split("/")

        begin_date = datetime.fromisoformat(begin)
        end_date = datetime.fromisoformat(end)

        if end_date < begin_date:
            raise PydanticValueError(
                "Begin date must be earlier than end date"
            )

    @root_validator
    def contains_or_intersects_or_bbox(cls, values):
        is_bbox = bool(values["bbox"])
        is_contains = bool(values["contains"])
        is_intersects = bool(values["intersects"])

        if sum((is_bbox, is_intersects, is_contains)) != 1:
            raise PydanticValueError(
                "One and only one of 'bbox', 'contains' or 'intersects'"
                "is allowed and required"
            )

    @root_validator
    def time_or_time_series(cls, values):
        is_time = bool(values["time"])
        is_time_series = bool(values["time_series"])

        if sum((is_time, is_time_series)) != 1:
            raise PydanticValueError(
                "One and only one of 'time' or 'time_series'"
                "is allowed and required"
            )

    @validator("time_series")
    def validate_time_series(cls, time_series: List[Tuple[str, str]]):
        for begin, end in time_series:
            begin_date = datetime.fromisoformat(begin)
            end_date = datetime.fromisoformat(end)

            if end_date < begin_date:
                raise PydanticValueError(
                    "Begin date must be earlier than end date"
                )
