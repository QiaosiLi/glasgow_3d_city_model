import os
from helper_ply import read_ply
import trimesh
import pandas as pd
import numpy as np
from sklearn.neighbors import KDTree


def compare_pc_lod2(pc_file, lod2_file):
    ply_z = read_ply(ply_file)['z']
    ply_z_min = np.min(ply_z)
    ply_z_max = np.max(ply_z)
    pt_num = ply_z.shape[0]
    try:
        mesh = trimesh.load_mesh(obj_file)
        obj_z_min = mesh.vertices[:,2].min()
        obj_z_max = mesh.vertices[:,2].max()
    except:
        obj_z_min = 0
        obj_z_max = 0
        print('error')

    z_dif = (ply_z_max - ply_z_min) - (obj_z_max - obj_z_min)
    z_min_dif = ply_z_min - obj_z_min
    z_max_dif = ply_z_max - obj_z_max
    return (pt_num, ply_z_min, ply_z_max, obj_z_min, obj_z_max, z_dif, z_min_dif, z_max_dif)


def calculate_normal_vector(vertex1, vertex2, vertex3):
    """
    Calculate the normal vector of a plane defined by three vertices.

    Parameters:
        vertex1 (numpy array): Coordinates of the first vertex.
        vertex2 (numpy array): Coordinates of the second vertex.
        vertex3 (numpy array): Coordinates of the third vertex.

    Returns:
        numpy array: Normal vector of the plane.
    """
    # Calculate two vectors on the plane by subtracting vertices
    edge1 = vertex2 - vertex1
    edge2 = vertex3 - vertex1

    # Calculate the cross product of the two vectors to get the normal vector
    normal_vector = np.cross(edge1, edge2)

    return normal_vector


def distance_point_to_plane(point, plane_normal, plane_point):
    """
    Calculate the distance between a point and a plane.

    Parameters:
        point (numpy array): Coordinates of the point.
        plane_normal (numpy array): Normal vector of the plane.
        plane_point (numpy array): Point on the plane.

    Returns:
        float: Distance between the point and the plane.
    """
    # Calculate the vector from the plane point to the given point
    vector_to_point = point - plane_point

    # Calculate the dot product of the vector to the point with the plane normal
    dot_product = np.dot(vector_to_point, plane_normal)

    # Calculate the magnitude of the plane normal
    normal_mag = np.linalg.norm(plane_normal)
    if np.isclose(normal_mag, 0):
        # Handle degenerate case where the plane is essentially a point
        # (e.g., two or more vertices are collinear or coincident)
        distance = np.linalg.norm(point - plane_point)
    else:
        # Calculate the distance
        distance = np.abs(dot_product) / normal_mag


    return distance


def calculate_rmse(obj_file, ply_file):
    mesh = trimesh.load(obj_file)
    vertices = mesh.vertices.view(np.ndarray)
    faces = mesh.faces.view(np.ndarray)

    # if mesh is not contitnue

    data = read_ply(ply_file)
    xyz = np.vstack((data['x'], data['y'], data['z'])).T

    # Mesh to Point Cloud RMSE: Calculate the RMSE from each vertex in the mesh to its nearest neighbor in the point cloud.
    xyz_tree = KDTree(xyz, leaf_size=50)
    dist_m2pc,_= xyz_tree.query(vertices, return_distance=True)
    rmse_m2pc = np.sqrt(np.mean(dist_m2pc ** 2))

    # Point Cloud to Mesh RMSE: Calculate the RMSE from each point in the point cloud to its nearest face in the mesh.
    vertices_tree = KDTree(vertices, leaf_size=50)
    vertices_idx = np.squeeze(vertices_tree.query(xyz, return_distance=False))

    dist_pc2m = []
    for i, idx in enumerate(vertices_idx):
        # print(i)
        point = xyz[i,:]
        rows = np.any(faces == idx, axis=1)
        near_faces = faces[rows]
        dist_p2f = []
        # for j, f in enumerate(near_faces):
        for f in near_faces:
            ver0 = vertices[f[0]]
            ver1 = vertices[f[1]]
            ver2 = vertices[f[2]]
            # Calculate the normal vector of the plane
            plane_normal = calculate_normal_vector(ver0, ver1, ver2)
            # Choose one vertex of the plane as a reference point
            plane_point = ver0
            # Calculate the distance between the point and the plane
            distance = distance_point_to_plane(point, plane_normal, plane_point)
            dist_p2f.append(distance)
        dist_p2f_min= np.min(dist_p2f)
        dist_pc2m.append(dist_p2f_min)

    rmse_pc2m = np.sqrt(np.mean(np.array(dist_pc2m) ** 2))

    return [rmse_m2pc, rmse_pc2m]


if __name__ == '__main__':

    main_folder = 'data/lod2'
    pkl_file = os.path.join(main_folder, 'table', 'footprints_rmse.pkl')
    df = pd.read_pickle(pkl_file)
    id_idx = df.index.tolist()

    for i in id_idx:
        id = df.iloc[i]['U_ID']
        print(id)
        tile_name = df.iloc[i]['tile_name']
        ply_file = os.path.join(main_folder, 'building_clip_ply', id + '.ply')
        obj_file = os.path.join(main_folder, 'output', id + '.obj')
        if not os.path.exists(obj_file):
            print('mesh does not exist')
            continue
        try:
            mesh = trimesh.load_mesh(obj_file)
            df.loc[i, 'obj_z_min'] = mesh.vertices[:, 2].min()
            df.loc[i, 'obj_z_max'] = mesh.vertices[:, 2].max()
        except:
            df.loc[i, 'obj_z_min'] = 0
            df.loc[i, 'obj_z_max'] = 0
            print('load mesh failed')
            continue
        ## calucate difference in Z values
        results = compare_pc_lod2(ply_file, obj_file)
        df.loc[i, ['pt_num','ply_z_min', 'ply_z_max', 'obj_z_min', 'obj_z_max', 'z_dif', 'z_min_dif', 'z_max_dif']] = results
        ## calucate RMSE
        rmse = calculate_rmse(obj_file, ply_file)
        print(rmse)
        df.loc[i, 'rmse_m2pc'] = rmse[0]
        df.loc[i, 'rmse_pc2m'] = rmse[1]
        df.to_pickle(pkl_file)

