import os
import geopandas as gpd
import pandas as pd
import glob
import fiona

def cal_iou(shapefile1, shapefile2, intersect_file, union_file):
    gdf1 = gpd.read_file(shapefile1)
    gdf2 = gpd.read_file(shapefile2)
    intersect_gdf = gpd.overlay(gdf1, gdf2, how='intersection')
    intersect_gdf.to_file(intersect_file)
    sum_area_intersect = 0
    for geom in intersect_gdf.geometry:
        sum_area_intersect += geom.area

    union_gdf = gpd.overlay(gdf1, gdf2, how='union')
    union_gdf.to_file(union_file)
    sum_area_union = 0
    for geom in union_gdf.geometry:
        sum_area_union += geom.area

    iou = sum_area_intersect / sum_area_union
    return [sum_area_intersect, sum_area_union, iou]

def cal_iou2(gdf1, shapefile2, intersect_file, union_file):
    # gdf1 = gpd.read_file(shapefile1)
    gdf2 = gpd.read_file(shapefile2)
    intersect_gdf = gpd.overlay(gdf1, gdf2, how='intersection')
    intersect_gdf.to_file(intersect_file)
    sum_area_intersect = 0
    for geom in intersect_gdf.geometry:
        sum_area_intersect += geom.area

    union_gdf = gpd.overlay(gdf1, gdf2, how='union')
    union_gdf.to_file(union_file)
    sum_area_union = 0
    for geom in union_gdf.geometry:
        sum_area_union += geom.area

    iou = sum_area_intersect / sum_area_union
    return [sum_area_intersect, sum_area_union, iou]


if __name__ == '__main__':

    main_folder = 'data/building_lod1/validation/footprints'

    gdb_path = 'data/building_footprints/building_footprints.gdb'
    feature_classes = fiona.listlayers(gdb_path)
    gdfs = []
    for fc in feature_classes:
        gdf = gpd.read_file(gdb_path, layer=fc)
        gdfs.append(gdf)
        merged_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))

    output_shapefile = os.path.join(main_folder, 'footprints_merge.shp')
    merged_gdf.to_file(output_shapefile)

    source_files = glob.glob(os.path.join(main_folder, 'shapefile/validation_source/*.shp'))
    source_name = []
    intersect = []
    union = []
    iou = []
    for file in source_files:
        name = os.path.basename(file).rsplit('_')[0]
        print(name)
        intersect_file = os.path.join(main_folder, 'shapefile', 'footprintmerge' + '_' + name + '_intersect.shp')
        union_file = os.path.join(main_folder, 'shapefile', 'footprintmerge' + '_' + name + '_union.shp')
        result = cal_iou2(merged_gdf, file, intersect_file, union_file)
        source_name.append(name)
        intersect.append(result[0])
        union.append(result[1])
        iou.append(result[2])

    results_df = pd.DataFrame({
        'name': source_name,
        'sum_intersect': intersect,
        'sum_union': union,
        'iou': iou
    })
    results_file = os.path.join(main_folder, 'table', 'footprintmerge_iou.csv')
    results_df.to_csv(results_file)

