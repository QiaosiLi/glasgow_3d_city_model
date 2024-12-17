import arcpy
import os
import glob

footprint_folder = 'E:/QL_2022/lidar_3d_city_modelling/building_lod1/validation/height/footprints'
footprint_list = glob.glob(os.path.join(footprint_folder, '*.shp'))
os_bh_file = 'E:/QL_2022/lidar_3d_city_modelling/building_lod1/validation/source_data/os_building_height/os_building_height_merge_380876.shp'
uk_building_file = 'E:/QL_2022/lidar_3d_city_modelling/building_lod1/validation/source_data/uk_buildings/uk_buildings_281765.shp'
out_folder = 'E:/QL_2022/lidar_3d_city_modelling/building_lod1/validation/height/spatial_join_results'
for fp in footprint_list:
    tile_name = os.path.basename(fp).rsplit('_')[0]
    print(tile_name)
    out_file_1 = os.path.join(out_folder, tile_name + '_osbh.shp')
    arcpy.analysis.SpatialJoin(target_features=fp,
                               join_features=os_bh_file,
                               out_feature_class=out_file_1,
                               join_operation="JOIN_ONE_TO_MANY",
                               join_type="KEEP_ALL",
                               match_option="INTERSECT")
    print('file1 saved')


