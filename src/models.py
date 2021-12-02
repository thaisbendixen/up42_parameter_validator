from datetime import datetime
from typing import List, Optional, Tuple

from geojson_pydantic.geometries import Geometry
from pydantic import BaseModel, Field, root_validator, validator


class DataModel(BaseModel):
    ids: Optional[List[str]]

    bbox: Optional[Tuple[float, float, float, float]]
    contains: Optional[Geometry]
    intersects: Optional[Geometry]

    limit: Optional[int] = Field(1, ge=1, le=500)

    zoom_level: Optional[int] = Field(18, ge=10, le=18)

    time_series: Optional[List[Tuple[str, str]]]
    time: Optional[str]

    max_cloud_cover: Optional[int] = Field(100, ge=0, le=100)

    @staticmethod
    def check_begin_end_date(begin: str, end: str):
        begin_date = datetime.fromisoformat(begin)
        end_date = datetime.fromisoformat(end)

        if end_date < begin_date:
            raise ValueError("Begin date must be earlier than end date")

    @staticmethod
    def exact_one_of(parameters: List[str], values: dict):
        total_sum = 0

        for parameter in parameters:
            total_sum += bool(values.get(parameter))

        if total_sum != 1:
            raise ValueError(f"Exact one of {parameters} is allowed")

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
            raise ValueError("Bbox not in WGS84 bounds [±180; ±90]")

        return bbox

    @validator("time")
    def validate_time(cls, time: str):
        begin, end = time.split("/")
        cls.check_begin_end_date(begin, end)

        return time

    @root_validator
    def check_mutually_exclusive_values(cls, values):
        cls.exact_one_of(["bbox", "contains", "intersects"], values)
        cls.exact_one_of(["time", "time_series"], values)

        return values

    @validator("time_series")
    def validate_time_series(cls, time_series: List[Tuple[str, str]]):
        for begin, end in time_series:
            cls.check_begin_end_date(begin, end)

        return time_series


class ModelWithPanchromatic(DataModel):
    panchromatic_band: bool = False


class Blocks(BaseModel):
    oneatlas_spot_aoiclipped: Optional[ModelWithPanchromatic] = Field(
        alias="oneatlas-spot-aoiclipped:1"
    )
    oneatlas_pleiades_aoiclipped: Optional[ModelWithPanchromatic] = Field(
        alias="oneatlas-pleiades-aoiclipped:1"
    )
    sobloo_s2_l1c_fullscene: Optional[DataModel] = Field(
        alias="sobloo-s2-l1c-fullscene:1"
    )
