import geopandas as gpd
import trimesh
import os
import fiona

main_folder = 'data/building_products'
gdb_path = os.path.join(main_folder, 'building_footprints', 'building_footprints.gdb') # path of building footrpint stored in geodatabase
feature_classes = fiona.listlayers(gdb_path)
for fc in feature_classes:
    print(fc)
    gdf = gpd.read_file(gdb_path, layer=fc)

    mesh_folder = os.path.join(main_folder, 'lod1_3d_building_model', '3d_mesh', fc)
    if not os.path.exists(mesh_folder):
        os.makedirs(mesh_folder)

    for idx,g in gdf['geometry'].iteritems():
        # footprint id
        id = gdf.loc[idx, 'U_ID']
        print(id)
        # building height
        h = gdf.loc[idx, 'MEAN']
        # ground height
        ground_z = gdf.loc[idx, 'Ground_Z']
        # footprint polygon
        if g.geom_type == 'MultiPolygon':
            mesh_list = []
            for polygon in g.geoms:
                out_mesh = trimesh.creation.extrude_polygon(polygon, height=h)
                mesh_list.append(out_mesh)
            extrude_mesh = trimesh.util.concatenate(mesh_list)
        else:
            extrude_mesh = trimesh.creation.extrude_polygon(g, height=h)

        extrude_mesh.vertices[:, 2] += ground_z
        out_file = os.path.join(mesh_folder, id + '.obj')
        extrude_mesh.export(out_file)



