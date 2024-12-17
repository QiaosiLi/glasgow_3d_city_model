import os
import arcpy

workspace = r"E:/QL_2022/lidar_3d_city_modelling/building_lod1/basic_editing_tiles/basic_editing_footrpints.gdb"
arcpy.env.workspace = workspace
featureclasses = arcpy.ListFeatureClasses()

print(featureclasses)

for fc in featureclasses:
    print(fc)
    fields = arcpy.ListFields(fc)
    tile_name = 'tile_name'
    field_exists = any(field.name == tile_name for field in fields)
    if not field_exists:
        arcpy.AddField_management(fc, tile_name, "TEXT", field_length=20)
        arcpy.management.CalculateField(fc, tile_name, f"'{fc}'", "PYTHON3")
        print('tile_name done')
    if field_exists:
        print('tile_name exists')
        
    uid_name = 'U_ID'
    field_exists = any(field.name == uid_name for field in fields)
    if not field_exists:
        arcpy.AddField_management(fc, uid_name, "TEXT", field_length=30)
        expression = "!tile_name! + '_' + str(!OBJECTID!)"
        arcpy.management.CalculateField(fc, uid_name, expression, "PYTHON3")
        print('uid done')
    if field_exists:
        print('uid exists')
  

fields_to_keep = ['tile_name', 'U_ID', 'Remark', 'Shape_Length','Shape_Area', 'OBJECTID','Shape']
for fc in featureclasses:
    print(fc)
    fields = arcpy.ListFields(fc)
    
    # Loop through all fields in the feature class
    for field in fields:
        # If the field is not in the fields_to_keep list, delete it
        if field.name.lower() not in [f.lower() for f in fields_to_keep]:
            arcpy.DeleteField_management(fc, field.name)
            print(f"Deleted field: {field.name}")
    

from arcpy.sa import *
bh_raster = 'E:/QL_2022/lidar_3d_city_modelling/grids/whole_area/MergeGrid23_50CM_BH.tif'
for fc in featureclasses[1:]:
    print(fc)
    outTable = os.path.join('E:/QL_2022/lidar_3d_city_modelling/building_lod1/basic_editing_tiles', fc+ '_bh.dbf')
    outTableName = fc + '_bh'
    outZSaT = ZonalStatisticsAsTable(fc, "U_ID", bh_raster, outTable, 'DATA',  'ALL')
    fc_joined = arcpy.management.AddJoin(fc, 'U_ID', outTable, 'U_ID')
    fields = {
        'MIN': outTableName + '.MIN',
        'MAX': outTableName + '.MAX',
        'RANGE':outTableName + '.RANGE',
        'MEAN': outTableName + '.MEAN',
        'STD': outTableName + '.STD',
        'SUM': outTableName + '.SUM',
        'MEDIAN': outTableName + '.MEDIAN',
        'PCT90': outTableName + '.PCT90'
    }

    # Add each field and calculate its value from the joined table
    for field, join_field in fields.items():
        arcpy.AddField_management(fc, field, 'DOUBLE')
        arcpy.CalculateField_management(fc, field, f"!{join_field}!", "PYTHON3")
    # Remove the join after calculations if it's no longer needed
    arcpy.management.RemoveJoin(fc, outTableName)

import os
import arcpy
from arcpy.sa import *

workspace = r"E:/QL_2022/lidar_3d_city_modelling/building_lod1/basic_editing_tiles/basic_editing_footrpints.gdb"
arcpy.env.workspace = workspace
featureclasses = arcpy.ListFeatureClasses()
print(featureclasses)


dtm_folder = r'E:/QL_2022/lidar_3d_city_modelling/original_data/Grids/DTM/5x5km/COG-LZW'

for fc in featureclasses:
    print(fc)
    dtm_raster = os.path.join(dtm_folder, fc + '_50CM_DTM_PHASE5.tif')
    outTable = os.path.join('E:/QL_2022/lidar_3d_city_modelling/building_lod1/basic_editing_tiles', fc + '_zmin.dbf')
    outTableName = fc + '_zmin'
    outZSaT = ZonalStatisticsAsTable(fc, "U_ID", dtm_raster, outTable, 'DATA', 'Minimum')
    fc_joined = arcpy.management.AddJoin(fc, 'U_ID', outTable, 'U_ID')
    fields = {
        'Ground_Z': outTableName + '.MIN'
       }

    # Add each field and calculate its value from the joined table
    for field, join_field in fields.items():
        arcpy.AddField_management(fc, field, 'DOUBLE')
        arcpy.CalculateField_management(fc, field, f"!{join_field}!", "PYTHON3")
    # Remove the join after calculations if it's no longer needed
    arcpy.management.RemoveJoin(fc, outTableName)
break


