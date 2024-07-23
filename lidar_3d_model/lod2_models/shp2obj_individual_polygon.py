import geopandas as gpd
import os
from shapely.geometry import Polygon, MultiPolygon



def shp_to_obj(shp_filepath, output_folder):
    gdf = gpd.read_file(shp_filepath)

    for idx,g in gdf['geometry'].iteritems():
        id = gdf.loc[idx, 'U_ID']
        z_min = gdf.loc[idx,'Ground_Z']
        print(id)

        if g.geom_type == 'Polygon':
            obj_filename = f"{output_folder}/{id}.obj"

            with open(obj_filename, 'w') as obj_file:
                vertex_counter = 1

                # Handle exterior
                exterior_coords = g.exterior.coords[:]
                # Write vertices for the exterior to the OBJ file
                for x, y in exterior_coords:
                    obj_file.write(f"v {x} {y} {z_min}\n")

                # Write face definition for the exterior
                vertex_end_index = vertex_counter + len(exterior_coords) - 1
                obj_file.write(f"f {' '.join(map(str, range(vertex_counter, vertex_end_index + 1)))}\n")

                vertex_counter += len(exterior_coords)

                # Handle holes (interiors)
                for interior in g.interiors:
                    interior_coords = interior.coords[:]
                    # Write vertices for the hole to the OBJ file
                    for x, y in interior_coords:
                        obj_file.write(f"v {x} {y} {z_min}\n")

                    # Write face definition for the hole
                    vertex_end_index = vertex_counter + len(interior_coords) - 1
                    obj_file.write(f"f {' '.join(map(str, range(vertex_counter, vertex_end_index + 1)))}\n")

                    vertex_counter += len(interior_coords)

        if g.geom_type == 'MultiPolygon':
        # for i, polygon in enumerate(geom):
            for polygon in g.geoms:
                # Create an individual OBJ file for each polygon
                obj_filename = f"{output_folder}/{id}.obj"

                with open(obj_filename, 'w') as obj_file:
                    vertex_counter = 1

                    # Handle exterior
                    exterior_coords = polygon.exterior.coords[:]
                    # Write vertices for the exterior to the OBJ file
                    for x, y in exterior_coords:
                        obj_file.write(f"v {x} {y} {z_min}\n")

                    # Write face definition for the exterior
                    vertex_end_index = vertex_counter + len(exterior_coords) - 1
                    obj_file.write(f"f {' '.join(map(str, range(vertex_counter, vertex_end_index + 1)))}\n")

                    vertex_counter += len(exterior_coords)

                    # Handle holes (interiors)
                    for interior in polygon.interiors:
                        interior_coords = interior.coords[:]
                        # Write vertices for the hole to the OBJ file
                        for x, y in interior_coords:
                            obj_file.write(f"v {x} {y} {z_min}\n")

                        # Write face definition for the hole
                        vertex_end_index = vertex_counter + len(interior_coords) - 1
                        obj_file.write(f"f {' '.join(map(str, range(vertex_counter, vertex_end_index + 1)))}\n")

                        vertex_counter += len(interior_coords)
    print('save')


if __name__ == '__main__':

    shp_filepath = "data/footprint/footprint.shp"
    output_path = "data/lod2/footprint_z"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    shp_to_obj(shp_filepath, output_path)
    print('obj files saved')

    # df = gpd.read_file(shp_filepath).drop('geometry', axis=1)
    # df_file = "data/lod2/table/footprints_z.pkl"
    # df.to_pickle(df_file)

