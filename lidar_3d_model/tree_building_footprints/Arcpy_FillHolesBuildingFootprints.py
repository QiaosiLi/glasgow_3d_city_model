import os
import glob
import arcpy

if __name__ == '__main__':

    data_folder = 'E:\\QL_2022\\lidar_3d_city_modelling\\building_lod1\\Building_Footprints\\BF_Revision'
    shp_list = glob.glob(os.path.join(data_folder, '*', '*_Building_Polygon_Greater20_FillHoles10.shp'))
    for input_file in shp_list:
        output_file = input_file.replace('_FillHoles10.shp', '_FillHoles10_Reg.shp')
        arcpy.ddd.RegularizeBuildingFootprint(in_features=input_file, out_feature_class=output_file,
                                              method="ANY_ANGLE", tolerance=1, densification=1, precision=0.05,
                                              diagonal_penalty=2, min_radius=0.1, max_radius=1000000,
                                              alignment_feature="", alignment_tolerance="", tolerance_type="DISTANCE")
    print('done')
        


