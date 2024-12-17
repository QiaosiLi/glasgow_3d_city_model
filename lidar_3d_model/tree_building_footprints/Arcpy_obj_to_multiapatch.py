import arcpy
import os
import glob


if __name__ == '__main__':

    main_folder = 'E:/QL_2022/UBDC_data_catalogue_3d_city/building_products/lod1_3d_building_model_part2'
    folders = glob.glob(os.path.join(main_folder, '3d_mesh/*'))
    for folder in folders[1:]:
        name = os.path.basename(folder)
        print(name)
        out_file = os.path.join(main_folder, 'building_model_lod1_part2.gdb', name)
        arcpy.ddd.Import3DFiles(in_files=folder , out_featureClass=out_file, root_per_feature="ONE_ROOT_ONE_FEATURE",
                                spatial_reference="PROJCS[\"British_National_Grid\",GEOGCS[\"GCS_OSGB_1936\",DATUM[\"D_OSGB_1936\",SPHEROID[\"Airy_1830\",6377563.396,299.3249646]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"False_Easting\",400000.0],PARAMETER[\"False_Northing\",-100000.0],PARAMETER[\"Central_Meridian\",-2.0],PARAMETER[\"Scale_Factor\",0.9996012717],PARAMETER[\"Latitude_Of_Origin\",49.0],UNIT[\"Meter\",1.0]];-5220400 -15524400 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision",
                                y_is_up="Z_IS_UP", file_suffix="OBJ", in_featureClass="", symbol_field="")
    print('done')


