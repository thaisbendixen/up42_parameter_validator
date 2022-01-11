from datetime import datetime
from typing import List, Optional, Tuple

import extra as extra
from geojson_pydantic.geometries import Geometry
from pydantic import BaseModel, Field, root_validator, validator
from processing_models import *


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
    tiling: Optional[Tiling] = Field(
        alias="tiling:1"
    )
    snap_polarimetric: Optional[SnapPolarimetric] = Field(
        alias="snap-polarimetric:1"
    )
    pansharpen: Optional[Pansharpen] = Field(
        alias="pansharpen:1"
    )
    crs_conversion: Optional[DataModel] = Field(
        alias="conversion:1"
    )
    data_conversion_dimap: Optional[DataConversionDimap] = Field(
        alias="data-conversion-dimap:1"
    )
    ndvi: Optional[NDVI] = Field(
        alias="ndvi:1"
    )
    oil_slick: Optional[OilSlick] = Field(
        alias="oil-slick:1"
    )
    ship_identification: Optional[ShipIdentification] = Field(
        alias="ship-identification:1"
    )
    snapship: Optional[Snapship] = Field(
        alias="snapship:1"
    )
    s5p_lvl3: Optional[S5pLvl3] = Field(
        alias="s5p-lvl3:1"
    )
    zonal_statistics: Optional[ZonalStatistics] = Field(
        alias="zonal-statistics:1"
    )
    vectorising: Optional[Vectorising] = Field(
        alias="vectorising:1"
    )
    augmentor: Optional[Augmentor] = Field(
        alias="augmentor:1"
    )
    up42_timeseries_image_statistics: Optional[TimeseriesImageStatistics] = Field(
        alias="up42-timeseries-image-statistics:1"
    )
    catalystpro_insstack: Optional[CatalystproInsstack] = Field(
        alias="catalystpro-insstack:1"
    )
    up42_terrasar_geotiff_conversion: Optional[TerrasarGeotiffConversion] = Field(
        alias="up42-terrasar-geotiff-conversion:1"
    )
    fertilization_zoning_map: Optional[FertilizationZoningMap] = Field(
        alias="fertilization-zoning-map:1"
    )
    up42_pools_detector: Optional[PoolDetector] = Field( # TODO careful here
        alias="dymaxionlabs/up42-pools-detector:1"
    )
    sharpening: Optional[Sharpening] = Field(
        alias="sharpening:1"
    )
    kmeans_clustering: Optional[KMeansClustering] = Field(
        alias="kmeans-clustering:1"
    )
    s2_superresolution: Optional[S2Superresolution] = Field(
        alias="s2-superresolution:1"
    )
    change_detector: Optional[ChangeDetector] = Field(
        alias="change_detector:1"
    )
    geocodis_builtup: Optional[GeocodisBuiltup] = Field(
        alias="geocodis-builtup:1"
    )
    terracover_realsat: Optional[TerracoverRealsat] = Field(
        alias="terracover-realsat:1"
    )
    up42_ndvithreshold: Optional[NdviThreshold] = Field(
        alias="up42-ndvithreshold:1"
    )
    landcover: Optional[Landcover] = Field(
        alias="landcover:1"
    )
    rfviewshed: Optional[RfViewshed] = Field(
        alias="rfviewshed:1"
    )
    viewshed: Optional[Viewshed] = Field(
        alias="viewshed:1"
    )
    superresolution: Optional[Superresolution] = Field(
        alias="superresolution:1"
    )
    qzsolutions_ndvi: Optional[QzsolutionsNdvi] = Field(
        alias="qzsolutions.ndvi:1"
    )
    qzsolutions_arvi: Optional[QzsolutionsArvi] = Field(
        alias="qzsolutions.arvi:1"
    )
    qzsolutions_nbr: Optional[QzsolutionsNbr] = Field(
        alias="qzsolutions.nbr:1"
    )
    qzsolutions_savi: Optional[QzsolutionsSavi] = Field(
        alias="qzsolutions.savi:1"
    )
    qzsolutions_mixer: Optional[QzsolutionsMixer] = Field(
        alias="qzsolutions.mixer:1"
    )
    qzsolutions_cigreen: Optional[Qzsolutions] = Field(
        alias="qzsolutions.cigreen:1"
    )
    qzsolutions_evi: Optional[Qzsolutions] = Field(
        alias="qzsolutions.evi:1"
    )
    qzsolutions_sipi: Optional[Qzsolutions] = Field(
        alias="qzsolutions.sipi:1"
    )

    # storage_tank: Optional[BaseModel] = Field(
    #     alias="storage_tank:1"
    # )

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"