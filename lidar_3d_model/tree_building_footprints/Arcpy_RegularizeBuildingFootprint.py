import os
import glob
import arcpy

if __name__ == '__main__':

    grid_folder = 'data\Building_Footprints' # The folder contains outputs of 'Arcpy_RasterToPolygon.py' .
    grid_list = glob.glob(os.path.join(grid_folder, '*', ''))
    for grid in grid_list:
        grid_name = grid.split('\\')[-2]
        print(grid_name)
        input_file = os.path.join(grid_folder, grid_name, grid_name + '_Building_Polygon_Greater20_FillHoles10.shp')
        output_file = os.path.join(grid_folder, grid_name, grid_name + '_Building_Polygon_Greater20_FillHoles10_Reg.shp')
        arcpy.ddd.RegularizeBuildingFootprint(in_features=input_file, out_feature_class=output_file,
                                              method="ANY_ANGLE", tolerance=1, densification=1, precision=0.05,
                                              diagonal_penalty=2, min_radius=0.1, max_radius=1000000,
                                              alignment_feature="", alignment_tolerance="", tolerance_type="DISTANCE")