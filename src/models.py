from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class BlockTypeEnum(str, Enum):
    data = "DATA"
    processing = "PROCESSING"


class DataModel(BaseModel):
    ids: Optional[str] = None
    bbox: list # validate with: shapely.geometry.box(*bbox) using shapely.geometry import box
    contains: dict # validate with: shape(contains) using shapely.geometry import shape
    intersects: dict  # validate with: shape(contains) using shapely.geometry import shape
    zoom_level: int = 18
    time_series: Optional[List[str]] = None # validate with datetime package
    time: str # validate with datetime package
    max_cloud_cover: int = 100
