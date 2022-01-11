def check_satellite_match(data_block, satellite):
    matches = {
        "oneatlas-pleiades-fullscene:1": "Pleiades Download",
        "oneatlas-spot-fullscene:1": "SPOT 6/7 Download",
        "oneatlas-spot-aoiclipped:1": "SPOT 6/7 Streaming",
        "sentinelhub-s2-aoiclipped:1": "Sentinel-2 Level 2 (BOA) AOI clipped",
        "sobloo-s2-l1c-fullscene:1": "Sentinel-2 L1C MSI Full Scenes",
        "sentinelhub-landsat8-aoiclipped:1": "Landsat-8 Level 1 (TOA)"
        " AOI clipped",
    }

    assert matches.get(data_block) == satellite


def check_geom_match(data_block_geom, processing_block_geom):
    assert data_block_geom
    assert processing_block_geom

    return True


BLOCKS_PARAMETER_REQUIREMENTS = {
    "coreg:1": {
        "data_block": {"limit": 2},
    },
    "orbital_pleiades_trucks:1": {
        "tiling:1": {
            "tile_width": 1232,
            "tile_height": 1232,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "buildingbox:1": {"crs-conversion:1": {"output_epsg_code": 3857}},
    "flood_mapping:1": {
        "snap-polarimetric:1": {
            "clip_to_aoi": True,
            "bbox": check_geom_match,
        }
    },
    "terracover-realsat:1": {
        "terracover-realsat:1": {
            "bbox": check_geom_match,
            "contains": None,
            "intersects": None,
        }
    },
    "shadow-detection:1": {
        "tiling:1": {
            "tile_width": 512,
            "tile_height": 512,
        }
    },
    "storage_tank:1": {
        "tiling:1": {
            "tile_width": 384,
            "tile_height": 384,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "orbital_pleiades_cars:1": {
        "tiling:1": {
            "tile_width": 1232,
            "tile_height": 1232,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "s2-superresolution:1": {
        "s2-superresolution:1": {
            "clip_to_aoi": True,
            "bbox": check_geom_match,
        }
    },
    "orbital_pleiades_aircraft:1": {
        "tiling:1": {
            "tile_width": 1024,
            "tile_height": 1024,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "building_extraction:1": {
        "tiling:1": {
            "tile_width": 768,
            "tile_height": 768,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "oil-slick:1": {
        "snap-polarimetric:1": {
            "clip_to_aoi": True,
            "bbox": check_geom_match,
            "linear_to_db": False,
            "speckle_filter": False,
        },
    },
    "dymaxionlabs/up42-pools-detector:1": {
        "tiling:1": {
            "tile_width": 256,
            "tile_height": 256,
        }
    },
    "fertilization-zoning-map:1": {
        "fertilization-zoning-map:1": {"intersects": check_geom_match}
    },
    "up42-countobjects:1": {
        "tiling:1": {
            "tile_width": 1232,
            "tile_height": 1232,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "catalystpro-insstack:1": {
        "catalystpro-insstack:1": {"aoi_geojson": check_geom_match}
    },
    "up42-timeseries-image-statistics:1": {
        "data_block": {
            # TODO S5 has to be max 1 month range
            "time": "2020-05-01T00:00:00+00:00/2020-05-31T23:59:59+00:00",
            "layer": "L3__AER_AI",
            "geojson_url": None,
        },
        "up42-timeseries-image-statistics:1": {"method": "mean"},
    },
    "advanced-water-related-geohazards-predictor:1": {
        "data_block": {"limit": 2}
    },
    "deforestation:1": {"data_block": {"limit": 2}},
    "up42-coregistration:1": {"data_block": {"limit": 2}},
    "snapship:1": {"snapship:1": {"bbox": check_geom_match}},
    "change-detection:1": {
        "data_block": {"limit": 2},
        "tiling:1": {
            "tile_width": 512,
            "tile_height": 512,
            "match_extents": True,
        },
    },
    "data-conversion-netcdf:1": {
        "meteomatics": {
            "bbox": check_geom_match,
        }
    },
    "hyperverge-changedetection-pleiades:1": {
        "data_block": {"limit": 2},
        "tiling:1": {
            "tile_width": 512,
            "tile_height": 512,
            "match_extents": True,
            "augmentation_factor": 2,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "hyperverge-changedetection-spot:1": {
        "data_block": {"limit": 2},
        "tiling:1": {
            "tile_width": 512,
            "tile_height": 512,
            "match_extents": True,
            "augmentation_factor": 2,
        },
        "crs-conversion:1": {"output_epsg_code": 3857},
    },
    "dra:1": {"data_block": {"limit": 2}},
    "change_detector:1": {"data_block": {"limit": 2}},
    "wind_turbines:1": {
        "tiling:1": {
            "tile_width": 256,
            "tile_height": 256,
            "augmentation_factor": 2,
        },
    },
    "building-height-detection:1": {
        "tiling:1": {"tile_width": 512, "tile_height": 512},
    },
    "qzsolutions.cigreen:1": {
        "qzsolutions.cigreen:1": {
            "satellite": check_satellite_match,
        },
    },
    "qzsolutions.evi:1": {
        "qzsolutions.evi:1": {
            "satellite": check_satellite_match,
        },
    },
    "qzsolutions.arvi:1": {
        "qzsolutions.arvi:1": {
            "satellite": check_satellite_match,
        },
    },
    "qzsolutions.savi:1": {
        "qzsolutions.savi:1": {
            "satellite": check_satellite_match,
        }
    },
    # TODO here we could compare bands with satellite used
    "qzsolutions.mixer:1": {
        "qzsolutions.mixer:1": {
            "red": "B08/256",
            "blue": "B04/256",
            "green": "B03/256",
            "satellite": check_satellite_match,
        }
    },
    "aiads_rgb_t3:1": {"data_block": {"limit": 5}},
    "buildingdetection:1": {
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
