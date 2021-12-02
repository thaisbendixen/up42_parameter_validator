from context import UP42ParamaterValidator

def test_check_parameters():
    input_parameters = {
        "oneatlas-spot-aoiclipped:1": {
            "ids": None,
            "time": "2018-01-01T00:00:00+00:00/2021-12-31T23:59:59+00:00",
            "limit": 1,
            "zoom_level": 17,
            "time_series": None,
            "max_cloud_cover": 100,
            "panchromatic_band": False,
            "contains": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [13.441429, 52.496578],
                        [13.385468, 52.479644],
                        [13.40126, 52.463331],
                        [13.464432, 52.477762],
                        [13.441429, 52.496578],
                    ]
                ],
            },
        },
        "tiling:1": {
            "tile_width": 732,
            "tile_height": 732,
            "match_extents": False,
            "augmentation_factor": 1,
        },
        "aiads_rgb_t3:1": {},
    }

    result = UP42ParamaterValidator(
        input_parameters=input_parameters
    ).check_parameters()

    assert isinstance(result, dict)
