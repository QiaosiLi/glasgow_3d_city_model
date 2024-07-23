from helper_ply import write_ply, read_ply
import laspy
import os
import glob
import numpy as np
import pandas as pd


def las2ply(las_path):
    las = laspy.read(las_path)
    classification = las.raw_classification
    if np.unique(classification) == 6:
        U_ID = os.path.basename(las_path).rsplit('.', 1)[0]
        xyz = las.xyz
        z_min = las.z.min()
        pts_num = xyz.shape[0]
        return [U_ID, xyz, z_min, pts_num]

if __name__ == '__main__':

    main_folder = 'data/lod2'
    las_path = os.path.join(main_folder, 'building_clip')  # folder contains clipped building point clouds in las format
    ply_path = os.path.join(main_folder,'building_clip_ply') # folder contains output building point clouds in ply format
    if not os.path.exists(ply_path):
        os.makedirs(ply_path)
    table_path = os.path.join(main_folder, 'table')
    pkl_file = os.path.join(table_path,  'footprints.pkl')
    df = pd.DataFrame(columns=['U_ID', 'z_min', 'pts_num'])

    las_files = glob.glob(os.path.join(las_path, '*.las'))
    for file in las_files:
        result = las2ply(file)
        ply_file = os.path.join(ply_path, result[0] + '.ply')
        write_ply(ply_file, [result[1]], ['x', 'y', 'z'])
        df = df.append({'U_ID': result[0], 'z_min': result[2], 'pts_num': result[3]}, ignore_index=True)
    print('ply files are saved.')
    # save table in a pkl file
    df = df.sort_values(by=['pts_num'])
    df = df.reset_index(drop=True)
    df.to_pickle(pkl_file)
    # save table in a txt file
    txt_file = os.path.join(table_path, 'footprints.txt')
    df.to_csv(txt_file)
    print('table is saved.')
