from typing import Literal

from pydantic import BaseModel, Field

# TODO what to do with individual repeated/reused parameters
# TODO maybe add literal colormaps


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
