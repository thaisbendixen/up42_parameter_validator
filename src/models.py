from typing import List, Optional

from pydantic import BaseModel


class DataModel(BaseModel):
    ids: Optional[str] = None
    # validate with: shapely.geometry.box(*bbox)
    bbox: list
    # validate with: shape(contains) using shapely.geometry import shape
    contains: dict
    # validate with: shape(contains) using shapely.geometry import shape
    intersects: dict
    zoom_level: int = 18
    time_series: Optional[List[str]] = None  # validate with datetime package
    time: str  # validate with datetime package
    max_cloud_cover: int = 100
