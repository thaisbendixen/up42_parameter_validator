# TODO what to do here
def check_satellite_match(data_block, satellite):
    try:
        if data_block == "oneatlas-pleiades-fullscene:1":
            assert satellite == "Pleiades Download"

        if data_block == "oneatlas-spot-fullscene:1":
            assert satellite == "SPOT 6/7 Download"

        if data_block == "oneatlas-spot-aoiclipped:1":
            assert satellite == "SPOT 6/7 Streaming"

        if data_block == "sentinelhub-s2-aoiclipped:1":
            assert satellite == "Sentinel-2 Level 2 (BOA) AOI clipped"

        if data_block == "sobloo-s2-l1c-fullscene:1":
            assert satellite == "Sentinel-2 L1C MSI Full Scenes"

        if data_block == "sentinelhub-landsat8-aoiclipped:1":
            assert satellite == "Landsat-8 Level 1 (TOA) AOI clipped"

    except AssertionError:
        pass


def check_geom_match(data_block_geom, processing_block_geom):
    is_match = True

    return is_match


def get_satellite_str(data_block):
    try:
        if data_block == "oneatlas-pleiades-fullscene:1":
            return "Pleiades Download"

        if data_block == "oneatlas-spot-fullscene:1":
            return "SPOT 6/7 Download"

        if data_block == "oneatlas-spot-aoiclipped:1":
            return "SPOT 6/7 Streaming"

        if data_block == "sentinelhub-s2-aoiclipped:1":
            return "Sentinel-2 Level 2 (BOA) AOI clipped"

        if data_block == "sobloo-s2-l1c-fullscene:1":
            return "Sentinel-2 L1C MSI Full Scenes"

        if data_block == "sentinelhub-landsat8-aoiclipped:1":
            return "Landsat-8 Level 1 (TOA) AOI clipped"

    except Exception:
        pass


BLOCKS_PARAMETER_REQUIREMENTS = {
    "coreg": {
        "data_block": {"limit": 2},
    },
    "orbital_pleiades_trucks": {
        "tiling:1": {
            "tile_width": 1232,
            "tile_height": 1232,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "buildingbox": {"crs-conversion:1": {"output_epsg_code": 3857}},
    "flood_mapping": {
        "snap-polarimetric:1": {
            "clip_to_aoi": True,
            "bbox": check_geom_match,
        }
    },
    "terracover-realsat": {
        "terracover-realsat:1": {
            "bbox": check_geom_match,
            "contains": None,
            "intersects": None,
        }
    },
    "shadow-detection": {
        "tiling:1": {
            "tile_width": 512,
            "tile_height": 512,
        }
    },
    "storage_tank": {
        "tiling:1": {
            "tile_width": 384,
            "tile_height": 384,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "orbital_pleiades_cars": {
        "tiling:1": {
            "tile_width": 1232,
            "tile_height": 1232,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "s2-superresolution": {
        "s2-superresolution:1": {
            "clip_to_aoi": True,
            "bbox": check_geom_match,
        }
    },
    "orbital_pleiades_aircraft": {
        "tiling:1": {
            "tile_width": 1024,
            "tile_height": 1024,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "building_extraction": {
        "tiling:1": {
            "tile_width": 768,
            "tile_height": 768,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "oil-slick": {
        "snap-polarimetric:1": {
            "clip_to_aoi": True,
            "bbox": check_geom_match,
            "linear_to_db": False,
            "speckle_filter": False,
        },
    },
    "dymaxionlabs/up42-pools-detector": {
        "tiling:1": {
            "tile_width": 256,
            "tile_height": 256,
        }
    },
    "fertilization-zoning-map": {
        "fertilization-zoning-map:1": {"intersects": check_geom_match}
    },
    "up42-countobjects": {
        "tiling:1": {
            "tile_width": 1232,
            "tile_height": 1232,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "catalystpro-insstack": {
        "catalystpro-insstack:1": {"aoi_geojson": check_geom_match}
    },
    "up42-timeseries-image-statistics": {
        "data_block": {
            "time": "2020-05-01T00:00:00+00:00/2020-05-31T23:59:59+00:00",  # TODO S5 has to be max 1 month range
            "layer": "L3__AER_AI",
            "geojson_url": None,
        },
        "up42-timeseries-image-statistics:1": {"method": "mean"},
    },
    "advanced-water-related-geohazards-predictor": {
        "data_block": {"limit": 2}
    },
    "deforestation": {"data_block": {"limit": 2}},
    "up42-coregistration": {"data_block": {"limit": 2}},
    "snapship": {"snapship:1": {"bbox": check_geom_match}},
    "change-detection": {
        "data_block": {"limit": 2},
        "tiling:1": {
            "tile_width": 512,
            "tile_height": 512,
            "match_extents": True,
        },
    },
    "data-conversion-netcdf": {
        "meteomatics": {
            "bbox": check_geom_match,
        }
    },
    "hyperverge-changedetection-pleiades": {
        "data_block": {"limit": 2},
        "tiling:1": {
            "tile_width": 512,
            "tile_height": 512,
            "match_extents": True,
            "augmentation_factor": 2,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "hyperverge-changedetection-spot": {
        "data_block": {"limit": 2},
        "tiling:1": {
            "tile_width": 512,
            "tile_height": 512,
            "match_extents": True,
            "augmentation_factor": 2,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "dra": {"data_block": {"limit": 2}},
    "change_detector": {"data_block": {"limit": 2}},
    "wind_turbines": {
        "tiling:1": {
            "tile_width": 256,
            "tile_height": 256,
            "augmentation_factor": 2,
        },
    },
    "building-height-detection": {
        "tiling:1": {"tile_width": 512, "tile_height": 512},
    },
    "qzsolutions.cigreen": {
        "qzsolutions.cigreen:1": {
            "satellite": check_satellite_match,
        },
    },
    "qzsolutions.evi": {
        "qzsolutions.evi:1": {
            "satellite": check_satellite_match,
        },
    },
    "qzsolutions.arvi": {
        "qzsolutions.arvi:1": {
            "satellite": check_satellite_match,
        },
    },
    "qzsolutions.savi": {
        "qzsolutions.savi:1": {
            "satellite": check_satellite_match,
        }
    },
    "qzsolutions.mixer": {  # TODO here we could compare bands with satellite used
        "qzsolutions.mixer:1": {
            "red": "B08/256",
            "blue": "B04/256",
            "green": "B03/256",
            "satellite": check_satellite_match,
        }
    },
    "aiads_rgb_t3": {"data_block": {"limit": 5}},
    "buildingdetection": {
        "data_block": {
            "time": None,
            "time_series": [
                "2020-08-01T00:00:00+00:00/2021-03-01T00:00:00+00:00",
                "2021-03-01T00:00:00+00:00/2021-09-01T00:00:00+00:00",
            ],
            "orbit_direction": "ASCENDING",
        }
    },
}
