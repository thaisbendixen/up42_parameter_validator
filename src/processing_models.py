from typing import Literal, List, Optional, Tuple

from geojson_pydantic.geometries import Geometry
from pydantic import BaseModel, Field, validator, PydanticValueError, BaseConfig, root_validator


# TODO what to do with individual repeated/reused parameters/validator
# TODO maybe add literals for colormaps

# def contains_or_intersects_or_bbox(values):
#     is_bbox = bool(values["bbox"])
#     is_contains = bool(values["contains"])
#     is_intersects = bool(values["intersects"])
#
#     if sum((is_bbox, is_intersects, is_contains)) > 1:  # TODO because here no geometry is also ok
#         raise PydanticValueError(
#             "One and only one of 'bbox', 'contains' or 'intersects'"
#             "is allowed and required"
#         )
#     # TODO I actually don't know if its required to define the parameters here
#
#     return values


# def is_clip_to_aoi(values):
#     is_bbox = bool(values["bbox"])
#     is_contains = bool(values["contains"])
#     is_intersects = bool(values["intersects"])
#     is_clip_to_aoi = bool(values["clip_to_aoi"])
#
#     if is_clip_to_aoi and sum((is_bbox, is_intersects, is_contains)) != 1:
#         raise PydanticValueError(
#             "If clip_to_aoi is set to True you must define a bbox, intersects or contains geometry"
#         )
#
#     return values

class Tiling(BaseModel):
    """
    block name
    tiling
    """
    nodata: int = 0 # TODO
    tile_width: int = Field(ge=1)
    tile_height: int = Field(ge=1)
    match_extents: bool = False
    output_prefix: str = ""
    augmentation_factor: int = Field(ge=1)
    discard_empty_tiles: bool = False

class SnapPolarimetric(BaseModel):
    """
    block name
    snap-polarimetric
    """
    bbox: Optional[Tuple[float, float, float, float]]
    contains: Optional[Geometry]
    intersects: Optional[Geometry]
    clip_to_aoi: bool = False
    mask: Optional[Literal["sea", "land"]] # TODO what happens when I select both
    tcorrection: bool = True
    calibration_band: Literal["signa", "beta", "gamma"] = "sigma" # TODO not sure here
    linear_to_db: bool = True
    speckle_filter: bool = True
    polarisations: List[str] = ['VV']

    # @validator("polarisations")
    # def check_polarisation(cls, polarisations): # TODO is it WGS?
    #     if not set(polarisations).issubset([["VV","VH"], ["HH", "HV"], ["VV"], ["VH"], ["HV"], ["HH"]]):
    #             raise PydanticValueError("The polarisation is not valid")
    #
    #     return polarisations
    #
    # @validator("bbox")
    # def bbox_in_WGS84_bounds(cls, bbox): # TODO is it WGS?
    #     if not all(
    #         [
    #             bbox[0] >= -180,
    #             bbox[1] >= -90,
    #             bbox[2] <= 180,
    #             bbox[3] <= 90,
    #         ]
    #     ):
    #         raise PydanticValueError("Bbox not in WGS84 bounds [±180; ±90]")
    #
    # # validators
    # _contains_or_intersects_or_bbox = validator('values', allow_reuse=True)(contains_or_intersects_or_bbox)
    # _is_clip_to_aoi = validator('values', allow_reuse=True)(is_clip_to_aoi)


class Pansharpen(BaseModel):
    """
    block name
    pansharpen
    """
    method: Literal["SFIM", "Brovey", "Esri"] = "SFIM"
    bbox: Optional[Tuple[float, float, float, float]]
    contains: Optional[Geometry]
    intersects: Optional[Geometry]
    clip_to_aoi: bool = False
    include_pan: bool = False

    @validator("bbox")
    def bbox_in_WGS84_bounds(cls, bbox): # TODO is it WGS?
        if not all(
            [
                bbox[0] >= -180,
                bbox[1] >= -90,
                bbox[2] <= 180,
                bbox[3] <= 90,
            ]
        ):
            raise PydanticValueError("Bbox not in WGS84 bounds [±180; ±90]")

    #validators
    # _contains_or_intersects_or_bbox = validator('values' ,allow_reuse=True)(contains_or_intersects_or_bbox)
    # _is_clip_to_aoi = validator('values', allow_reuse=True)(is_clip_to_aoi)
    @root_validator
    def contains_or_intersects_or_bbox(cls, values):
        is_bbox = bool(values["bbox"])
        is_contains = bool(values["contains"])
        is_intersects = bool(values["intersects"])

        if sum((is_bbox, is_intersects, is_contains)) > 1:  # TODO because here no geometry is also ok
            raise PydanticValueError(
                "One and only one of 'bbox', 'contains' or 'intersects'"
                "is allowed and required"
            )
        # TODO I actually don't know if its required to define the parameters here

        return values

    @root_validator
    def is_clip_to_aoi(cls, values):
        is_bbox = bool(values["bbox"])
        is_contains = bool(values["contains"])
        is_intersects = bool(values["intersects"])
        is_clip_to_aoi = bool(values["clip_to_aoi"])

        if is_clip_to_aoi and sum((is_bbox, is_intersects, is_contains)) != 1:
            raise PydanticValueError(
                "If clip_to_aoi is set to True you must define a bbox, intersects or contains geometry"
            )

        return values


class CrsConversion(BaseModel):
    """
    block name
    crs-conversion
    """
    output_epsg_code: Optional[int] = Field(ge=1024, le=32767)
    resampling_method: Literal["nearest", "bilinear", "cubic", "cubic_spline", "lanczos", "average", "mode"]  = "cubic"


class DataConversionDimap(BaseModel):
    """
    block name
    data-conversion-dimap
    """
    ms: Optional[bool]
    pan: Optional[bool]
    bbox: Optional[Tuple[float, float, float, float]]
    contains: Optional[Geometry]
    intersects: Optional[Geometry]
    clip_to_aoi: bool

    @validator("bbox")
    def bbox_in_WGS84_bounds(cls, bbox): # TODO is it WGS?
        if bbox:
            if not all(
                [
                    bbox[0] >= -180,
                    bbox[1] >= -90,
                    bbox[2] <= 180,
                    bbox[3] <= 90,
                ]
            ):
                raise PydanticValueError("Bbox not in WGS84 bounds [±180; ±90]")
        return bbox

    # validators
    # _contains_or_intersects_or_bbox = validator('values', allow_reuse=True)(contains_or_intersects_or_bbox)
    # _is_clip_to_aoi = validator('values', allow_reuse=True, always=True)(is_clip_to_aoi)

    @root_validator
    def contains_or_intersects_or_bbox(cls, values):
        is_bbox = bool(values["bbox"])
        is_contains = bool(values["contains"])
        is_intersects = bool(values["intersects"])

        if sum((is_bbox, is_intersects, is_contains)) > 1:  # TODO because here no geometry is also ok
            raise ValueError(
                "One and only one of 'bbox', 'contains' or 'intersects'"
                "is allowed and required"
            )
        # TODO I actually don't know if its required to define the parameters here

        return values

    @root_validator
    def is_clip_to_aoi(cls, values):
        is_bbox = bool(values["bbox"])
        is_contains = bool(values["contains"])
        is_intersects = bool(values["intersects"])
        is_clip_to_aoi = bool(values["clip_to_aoi"])

        if is_clip_to_aoi and sum((is_bbox, is_intersects, is_contains)) != 1:
            raise ValueError(
                "If clip_to_aoi is set to True you must define a bbox, intersects or contains geometry"
            )

        return values

class NDVI(BaseModel):
    """
    block name
    ndvi
    """
    output_original_raster: bool = False

class OilSlick(BaseModel):
    """
    block name
    oil-slick
    """
    bbox: bool = False

class ShipIdentification(BaseModel):
    """
    block name
    ship-identification
    """
    minutes: int = Field(15, ge=1, le=720)

class Snapship(BaseModel):
    """
    block name
    snapship
    """
    bbox: Optional[Tuple[float, float, float, float]]
    contains: Optional[Geometry]
    intersects: Optional[Geometry]
    maxsize: int = Field(50, ge=0, le=100)
    minsize: bool = False

    @validator("bbox")
    def bbox_in_WGS84_bounds(cls, bbox): # TODO is it WGS?
        if not all(
            [
                bbox[0] >= -180,
                bbox[1] >= -90,
                bbox[2] <= 180,
                bbox[3] <= 90,
            ]
        ):
            raise PydanticValueError("Bbox not in WGS84 bounds [±180; ±90]")

    # validators
    # _contains_or_intersects_or_bbox = validator('values', allow_reuse=True)(contains_or_intersects_or_bbox)

    @root_validator
    def contains_or_intersects_or_bbox(cls, values):
        is_bbox = bool(values["bbox"])
        is_contains = bool(values["contains"])
        is_intersects = bool(values["intersects"])

        if sum((is_bbox, is_intersects, is_contains)) > 1:  # TODO because here no geometry is also ok
            raise PydanticValueError(
                "One and only one of 'bbox', 'contains' or 'intersects'"
                "is allowed and required"
            )
        # TODO I actually don't know if its required to define the parameters here

        return values


class S5pLvl3(BaseModel):
    """
    block name
    s5p-lvl3
    """
    resolution: float = Field(0.1, ge=0.07) # TODO does this work
    min_quality_threshold: int = Field(50, ge=0, le=100)
    include_ancillary_bands: bool = False

class ZonalStatistics(BaseModel):
    """
    block name
    zonal-statistics
    """
    stats: List[str] = [
         "min",
         "max",
         "mean",
         "median",
         "std",
         "count",
         "std"
      ]
    zones: List[Geometry] = []
    zones_attribute_id: str = "stats_id" # TODO don't understant these parameters

    @validator("stats")
    def valid_stats(cls, stats):
        if not set(stats).issubset(["min", "max", "mean", "sum", "std", "median", "majority", "minority", "unique", "range", "nodata", "percentile_[0-100]", "count"]):
            raise PydanticValueError("Bbox not in WGS84 bounds [±180; ±90]")

        return stats

class Vectorising(BaseModel):
    """
    block name
    vectorising
    """
    n_sieve_pixels: int = 1

class Augmentor(BaseModel):
    """
    block name
    augmentor
    """
    denoising_factor: int = 0
    colour_denoising_factor: int = 10

class TimeseriesImageStatistics(BaseModel):
    """
    block name
    up42-timeseries-image-statistics
    """
    method: Literal["mean", "min", "max", "std", "median", "sum"] = "mean"


class CatalystproInsstack(BaseModel):
    """
    block name
    catalystpro-insstack
    """
    aoi_bbox: Optional[Tuple[float, float, float, float]] # TODO not sure about this one
    aoi_geojson: Optional[Geometry] # TODO not sure about this one

# TODO add check bbox or intersects
class TerrasarGeotiffConversion(BaseModel):
    """
    block name
    up42-terrasar-geotiff-conversion
    """
    bbox: Optional[Tuple[float, float, float, float]]
    intersects: Optional[Geometry]
    clip_to_aoi: bool = False

    @validator("bbox")
    def bbox_in_WGS84_bounds(cls, bbox): # TODO is it WGS?
        if not all(
            [
                bbox[0] >= -180,
                bbox[1] >= -90,
                bbox[2] <= 180,
                bbox[3] <= 90,
            ]
        ):
            raise PydanticValueError("Bbox not in WGS84 bounds [±180; ±90]")

        return bbox

    # validator
    # _is_clip_to_aoi = validator('values', allow_reuse=True, always=True)(is_clip_to_aoi)

    @root_validator
    def is_clip_to_aoi(cls, values):
        is_bbox = bool(values["bbox"])
        is_contains = bool(values["contains"])
        is_intersects = bool(values["intersects"])
        is_clip_to_aoi = bool(values["clip_to_aoi"])

        if is_clip_to_aoi and sum((is_bbox, is_intersects, is_contains)) != 1:
            raise PydanticValueError(
                "If clip_to_aoi is set to True you must define a bbox, intersects or contains geometry"
            )

        return values



class FertilizationZoningMap(BaseModel):
    """
    block name
    fertilization-zoning-map
    """
    intersects: Optional[Geometry]

# not sure about parameters here since block disabled
class PoolDetector(BaseModel):
    """
    block name
    dymaxionlabs/up42-pools-detector
    """
    strength: Literal["light", "medium", "strong"] = "medium"

class Sharpening(BaseModel):
    """
    block name
    sharpening
    """
    strength: Literal["light", "medium", "strong"] = "medium"

class KMeansClustering(BaseModel):
    """
    block name
    kmeans-clustering
    """
    n_clusters: int = 6
    n_iterations: int = 10
    n_sieve_pixels: int = 64

class S2Superresolution(BaseModel):
    """
    block name
    s2-superresolution
    """
    bbox: Optional[Tuple[float, float, float, float]]
    contains: Optional[Geometry]
    intersects: Optional[Geometry]
    clip_to_aoi: bool = False
    copy_original_bands: bool = True


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

        return bbox

    # validators
    # _contains_or_intersects_or_bbox = validator('values', allow_reuse=True)(contains_or_intersects_or_bbox)
    # _is_clip_to_aoi = validator('values', allow_reuse=True, always=True)(is_clip_to_aoi)

    @root_validator
    def contains_or_intersects_or_bbox(cls, values):
        is_bbox = bool(values["bbox"])
        is_contains = bool(values["contains"])
        is_intersects = bool(values["intersects"])

        if sum((is_bbox, is_intersects, is_contains)) > 1:  # TODO because here no geometry is also ok
            raise PydanticValueError(
                "One and only one of 'bbox', 'contains' or 'intersects'"
                "is allowed and required"
            )
        # TODO I actually don't know if its required to define the parameters here

        return values

    @root_validator
    def is_clip_to_aoi(cls, values):
        is_bbox = bool(values["bbox"])
        is_contains = bool(values["contains"])
        is_intersects = bool(values["intersects"])
        is_clip_to_aoi = bool(values["clip_to_aoi"])

        if is_clip_to_aoi and sum((is_bbox, is_intersects, is_contains)) != 1:
            raise PydanticValueError(
                "If clip_to_aoi is set to True you must define a bbox, intersects or contains geometry"
            )

        return values

class ChangeDetector(BaseModel):
    """
    block name
    change_detector
    """
    block_size: int = 5
    erode_size: int = 13


class GeocodisBuiltup(BaseModel):
    """
    block name
    geocodis-builtup
    """
    probabilities: bool = False


class TerracoverRealsat(BaseModel):
    """
    block name
    terracover-realsat
    """
    bbox: Optional[Tuple[float, float, float, float]]
    contains: Optional[Geometry]
    intersects: Optional[Geometry]

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

    # validators
    # _contains_or_intersects_or_bbox = validator('values', allow_reuse=True)(contains_or_intersects_or_bbox)

    @root_validator
    def contains_or_intersects_or_bbox(cls, values):
        is_bbox = bool(values["bbox"])
        is_contains = bool(values["contains"])
        is_intersects = bool(values["intersects"])

        if sum((is_bbox, is_intersects, is_contains)) > 1:  # TODO because here no geometry is also ok
            raise PydanticValueError(
                "One and only one of 'bbox', 'contains' or 'intersects'"
                "is allowed and required"
            )
        # TODO I actually don't know if its required to define the parameters here

        return values

class NdviThreshold(BaseModel):
    """
    block name
    up42-ndvithreshold
    """
    n_sieve_pixels: int = 5
    threshold_values: dict = {
            "no_vegetation":0.2,
            "dense_vegetation":0.9,
            "sparse_vegetation":0.4,
            "moderate_vegetation":0.6
         }

    @validator("threshold_values")
    def validate_threshold_values(cls, threshold_values: dict):
        for value in threshold_values.values():
            if value not in range(0,1):
                raise PydanticValueError(
                    f"The {value} dictionary value must be between 0 and 1"
                )
            return threshold_values

class Landcover(BaseModel):
    """
    block name
    landcover
    """
    nclasses: int = Field(5, ge=4, le=5)

class RfViewshed(BaseModel):
    """
    block name
    rfviewshed
    """

    power_dbm: float
    color_palette: str = "RYGCBM"
    frequency_mhz: float
    downtilt_degrees: float = Field(0.0, ge=-90, le=90)
    direction_degrees: float = Field(0.0, ge=0, le=360)
    receiver_gain_dbi: float = 0.0
    rain_loss_db_per_m: float = -9999.0
    max_distance_meters: float
    rain_rate_mm_per_hr: float = 0.0
    oxygen_loss_db_per_m: float = 0.0
    polarization_degrees: float = Field(0.0, ge=0, le=90)  # TODO not sure here
    transmitter_gain_dbi: float = 0.0
    transmitter_latitude: float
    transmitter_longitude: float
    receiver_height_meters: float = Field(0.0, ge=0, le=100)
    signal_strength_low_db: float = -70.0
    signal_strength_high_db: float = -30.0
    transmitter_height_meters: float = Field(0.0, ge=0, le=100)
    vertical_beamwidth_degrees: float = Field(180.0, ge=0, le=180)
    horizontal_beamwidth_degrees: float = 360.0


class Viewshed(BaseModel):
    """
    block name
    viewshed
    """

    observer_latitude: float = Field(1, ge=-90, le=90)
    observer_longitude: float = Field(1, ge=-180, le=180)
    max_distance_meters: float
    target_height_meters: float
    start_azimuth_degrees: float = Field(1, ge=0, le=360)
    end_azimuth_degrees: float = Field(1, ge=0, le=360)
    observer_height_meters: float


class Superresolution(BaseModel):
    """
    block name
    superresolution
    """

    model: Literal["SRCNN", "AESR", "RedNet"] = "SRCNN"


class QzsolutionsNdvi(BaseModel):
    """
    block name
    qzsolutions.ndvi
    """

    colormap: str = "qz_ndvi"
    satellite: Literal[
        "Pleiades Download",
        "SPOT 6/7 Download",
        "SPOT 6/7 Streaming",
        "Sentinel-2 Level 2 (BOA) AOI clipped",
        "Sentinel-2 L1C MSI Full Scenes",
        "Landsat-8 Level 1 (TOA) AOI clipped",
    ]


class QzsolutionsArvi(BaseModel):
    """
    block name
    qzsolutions.arvi
    """

    y: float = 0.1
    colormap: str = "RdYlGn"
    satellite: Literal[
        "Pleiades Download",
        "SPOT 6/7 Download",
        "SPOT 6/7 Streaming",
        "Sentinel-2 Level 2 (BOA) AOI clipped",
        "Sentinel-2 L1C MSI Full Scenes",
        "Landsat-8 Level 1 (TOA) AOI clipped",
    ]


class QzsolutionsNbr(BaseModel):
    """
    block name
    qzsolutions.nbr
    """

    colormap: str = "binary"
    satellite: Literal[
        "Pleiades Download",
        "SPOT 6/7 Download",
        "SPOT 6/7 Streaming",
        "Sentinel-2 Level 2 (BOA) AOI clipped",
        "Sentinel-2 L1C MSI Full Scenes",
        "Landsat-8 Level 1 (TOA) AOI clipped",
    ]


class QzsolutionsSavi(BaseModel):
    """
    block name
    qzsolutions.savi
    """

    L: float = 0.5
    colormap: str = "RdYlGn"
    satellite: Literal[
        "Pleiades Download",
        "SPOT 6/7 Download",
        "SPOT 6/7 Streaming",
        "Sentinel-2 Level 2 (BOA) AOI clipped",
        "Sentinel-2 L1C MSI Full Scenes",
        "Landsat-8 Level 1 (TOA) AOI clipped",
    ]


class QzsolutionsMixer(BaseModel):
    """
    block name
    qzsolutions.mixer
    """

    red: str
    blue: str
    green: str
    satellite: Literal[
        "Pleiades Download",
        "SPOT 6/7 Download",
        "SPOT 6/7 Streaming",
        "Sentinel-2 Level 2 (BOA) AOI clipped",
        "Sentinel-2 L1C MSI Full Scenes",
        "Landsat-8 Level 1 (TOA) AOI clipped",
    ]


class Qzsolutions(BaseModel):
    """
    block name
    qzsolutions.cigreen
    qzsolutions.evi
    qzsolutions.sipi
    """

    satellite: Literal[
        "Pleiades Download",
        "SPOT 6/7 Download",
        "SPOT 6/7 Streaming",
        "Sentinel-2 Level 2 (BOA) AOI clipped",
        "Sentinel-2 L1C MSI Full Scenes",
        "Landsat-8 Level 1 (TOA) AOI clipped",
    ]
