from src.up42_parameter_validator import UP42ParamaterValidator
from src.models import Blocks

def test_check_parameters():
    input_parameters = Blocks(oneatlas_spot_aoiclipped=None, oneatlas_pleiades_aoiclipped=None, sobloo_s2_l1c_fullscene=None, tiling=Tiling(nodata=0, tile_width=768, tile_height=768, match_extents=False, output_prefix='', augmentation_factor=1, discard_empty_tiles=True), snap_polarimetric=None, pansharpen=None, crs_conversion=None, data_conversion_dimap=DataConversionDimap(ms=True, pan=False, bbox=(13.364182, 52.486439, 13.395252, 52.499399), contains=None, intersects=None, clip_to_aoi=True), ndvi=None, oil_slick=None, ship_identification=None, snapship=None, s5p_lvl3=None, zonal_statistics=None, vectorising=None, augmentor=None, up42_timeseries_image_statistics=None, catalystpro_insstack=None, up42_terrasar_geotiff_conversion=None, fertilization_zoning_map=None, up42_pools_detector=None, sharpening=None, kmeans_clustering=None, s2_superresolution=None, change_detector=None, geocodis_builtup=None, terracover_realsat=None, up42_ndvithreshold=None, landcover=None, rfviewshed=None, viewshed=None, superresolution=None, qzsolutions_ndvi=None, qzsolutions_arvi=None, qzsolutions_nbr=None, qzsolutions_savi=None, qzsolutions_mixer=None, qzsolutions_cigreen=None, qzsolutions_evi=None, qzsolutions_sipi=None, oneatlas-spot-display:1={'asset_ids': None, 'contains': None, 'ids': None, 'limit': 1, 'max_cloud_cover': 100, 'time': '2018-01-01T00:00:00+00:00/2021-12-31T23:59:59+00:00', 'time_series': None}, crs-conversion:1={'output_epsg_code': None, 'resampling_method': 'cubic'}, storage_tank:1={})

    result = UP42ParamaterValidator(input_parameters=input_parameters).check_parameters()

    assert isinstance(result, dict)
