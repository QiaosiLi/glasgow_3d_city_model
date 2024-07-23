import os
import subprocess
import time
from datetime import date
import pandas as pd
from helper_ply import read_ply

exe_file = 'E://QL_2022//City3D_A//out/build//x64-Release//bin//CLI_Example_2_V2.exe'  # Path of city3d built exe file

csv_file = 'data/lod2_uid.csv'
df = pd.read_csv(csv_file)
id_idx = df.index.tolist()
pkl_file = 'data/lod2_uid.pkl'

timeout = 3600  # Stop to process if the processing time is longer than 1 hour
lambda_model_complexity = str(0.62)  # Turing complexity parameter here

j = 0
for i in id_idx:
    j += 1
    item_name = df.iloc[i]['U_ID']
    input_ply = os.path.join('data','building_clip_ply', item_name + '.ply')
    output_footprint_path = os.path.join('data', 'footprint_z_city3d')
    if not os.path.exists(output_footprint_path):
        os.makedirs(output_footprint_path)
    footprint_file = os.path.join(output_footprint_path, item_name + '.obj')
    output_folder = os.path.join('data', 'output')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file = os.path.join(output_folder, item_name + '.obj')

    # Setting parameters
    number_region_growing = str(df.iloc[i]['nrg'])  # Turing number of point for region growing here
    # number_region_growing = str(250)
    ply = read_ply(input_ply)
    ply_z_min = str(ply['z'].min())
    # ply_z_min = str(df.iloc[i]['z_min'])

    print("____________________________run city3d____________________________")
    print(f'{j} out of {len(id_idx)}')
    start_time = time.time()
    print(f"UID:{item_name}, Area:{df.iloc[i]['Shape_Area']}")
    # print(f"UID:{item_name}, number of point:{df.iloc[i]['pts_num']}")
    try:
        # run city3d
        return_code = subprocess.call([exe_file, input_ply, footprint_file, output_file, ply_z_min, number_region_growing, lambda_model_complexity], timeout=timeout)
        end_time = time.time()
        duration = end_time - start_time
        if return_code == 0:
            print(f"finished in {duration}s")
            df.loc[i, 'nrg'] = number_region_growing
            df.loc[i, 'result'] = 'succeed'
            df.loc[i, 'time'] = duration
            df.loc[i, 'lod2'] = date.today().strftime('%d/%m/%Y')
            df.loc[i, 'z_min'] = ply_z_min
            df.to_pickle(pkl_file)

        else:
            print(f"failed in {duration}s, return code = {return_code}")
            df.loc[i, 'nrg'] = number_region_growing
            df.loc[i, 'result'] = 'failed'
            df.loc[i, 'time'] = duration
            df.loc[i, 'z_min'] = ply_z_min
            df.to_pickle(pkl_file)
    except:
        print(f"timeout in {timeout}s")
        df.loc[i, 'nrg'] = number_region_growing
        df.loc[i, 'result'] = 'timeout'
        df.loc[i, 'time'] = timeout
        df.loc[i, 'z_min'] = ply_z_min
        df.to_pickle(pkl_file)

df.to_csv(csv_file)
print('done')


