from src.up42_parameter_validator import UP42ParamaterValidator


def test_check_parameters():
    input_parameters = {
      "oneatlas-spot-display:1": {
        "time": "2018-01-01T00:00:00+00:00/2021-12-31T23:59:59+00:00",
        "limit": 1,
        "asset_ids": None,
        "time_series": None,
        "max_cloud_cover": 100,
        "contains": {
          "type": "Polygon",
          "coordinates": [
            [
              [
                13.395767,
                52.519772
              ],
              [
                13.389587,
                52.513087
              ],
              [
                13.402634,
                52.510788
              ],
              [
                13.40641,
                52.515385
              ],
              [
                13.395767,
                52.519772
              ]
            ]
          ]
        }
      },
      "data-conversion-dimap:1": {
        "ms": True,
        "pan": False,
        "bbox": None,
        "contains": None,
        "intersects": None,
        "clip_to_aoi": True
      }
    }
    result = UP42ParamaterValidator(
        input_parameters=input_parameters
    ).check_parameters()

    assert isinstance(result, dict)
