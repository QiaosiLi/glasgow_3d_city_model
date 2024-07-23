import geopandas as gpd
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


## 20240614
main_folder = 'data/building_lod1/validation/height'
fp_file = 'data/building_lod1/validation/footprints/footprints_merge.shp'  # our footprint shapefile
gdf_fp = gpd.read_file(fp_file)

oshb_file = os.path.join(main_folder, 'spatial_join_4tiles_results', 'fp4tiles_oshb_groupby.shp') # spatial join and groupby of height attributes result of ordance survey building height data
gdf_oshb = gpd.read_file(oshb_file)
gdf_oshb_merge = gdf_fp.merge(gdf_oshb[['U_ID','abshmin', 'relh2', 'relhmax']], on='U_ID')
gdf_oshb_merge['d_ground'] = gdf_oshb_merge['abshmin']-gdf_oshb_merge['Ground_Z']
gdf_oshb_merge['d_rh2_mean'] = gdf_oshb_merge['relh2'] - gdf_oshb_merge['MEAN']
gdf_oshb_merge['d_rh2_med'] = gdf_oshb_merge['relh2'] - gdf_oshb_merge['MEDIAN']
gdf_oshb_merge['d_rmax_max'] = gdf_oshb_merge['relhmax'] - gdf_oshb_merge['MAX']
gdf_oshb_merge['d_rmax_90'] = gdf_oshb_merge['relhmax'] - gdf_oshb_merge['PCT90']
gdf_oshb_merge.to_file(oshb_file)
#
ukb_file = os.path.join(main_folder, 'spatial_join_4tiles_results', 'fp4tiles_ukb_groupby.shp') # spatial join and groupby of height attributes result of ukbuildings data
gdf_ukb = gpd.read_file(ukb_file)
gdf_ukb_merge = gdf_fp.merge(gdf_ukb[['U_ID', 'height_mea', 'height_max']], on='U_ID')
gdf_ukb_merge['d_hmean_mean'] = gdf_ukb_merge['height_mea'] - gdf_ukb_merge['MEAN']
gdf_ukb_merge.to_file(ukb_file)

## RMSE, r

def rmse(col1, col2):
    return np.sqrt(np.mean((col1-col2)**2))

rems_ground = rmse(gdf_oshb_merge['abshmin'],gdf_oshb_merge['Ground_Z'])
r_ground = gdf_oshb_merge['abshmin'].corr(gdf_oshb_merge['Ground_Z'])

results_df = pd.DataFrame({
    'Column': 'Ground_Z',
    'rmse_abshmin': [rems_ground],
    'r_absmin': [r_ground]
})

result_file = os.path.join(main_folder, 'statistical_results', 'osbh_absmin.csv')
results_df.to_csv(result_file)

rmse_relh2 = {}
r_relh2 ={}
rmse_relhmax = {}
r_relhmax ={}
osbh_vs_list = ['MIN', 'MAX', 'MEAN', 'MEDIAN', 'PCT90']
for col in osbh_vs_list:
    rmse_relh2[col] = rmse(gdf_oshb_merge['relh2'], gdf_oshb_merge[col])
    r_relh2[col] = gdf_oshb_merge['relh2'].corr(gdf_oshb_merge[col])
    rmse_relhmax[col] = rmse(gdf_oshb_merge['relhmax'], gdf_oshb_merge[col])
    r_relhmax[col] = gdf_oshb_merge['relhmax'].corr(gdf_oshb_merge[col])

results_df = pd.DataFrame({
    'Column': osbh_vs_list,
    'rmse_relh2': [rmse_relh2[col] for col in osbh_vs_list],
    'r_relh2': [r_relh2[col] for col in osbh_vs_list],
    'rmse_relhmax': [rmse_relhmax[col] for col in osbh_vs_list],
    'r_relhmax': [r_relhmax[col] for col in osbh_vs_list],
})

result_file = os.path.join(main_folder, 'statistical_results', 'osbh_relh2_relhmax.csv')
results_df.to_csv(result_file)


## ukb data
rmse_hmean = {}
r_hmean ={}
rmse_hmax = {}
r_hmax ={}

ukb_vs_list = ['MIN', 'MAX', 'MEAN', 'MEDIAN', 'PCT90']
for col in ukb_vs_list:
    rmse_hmean[col] = rmse(gdf_ukb_merge['height_mea'], gdf_ukb_merge[col])
    r_hmean[col] = gdf_ukb_merge['height_mea'].corr(gdf_ukb_merge[col])
    rmse_hmax[col] = rmse(gdf_ukb_merge['height_max'], gdf_ukb_merge[col])
    r_hmax[col] = gdf_ukb_merge['height_max'].corr(gdf_ukb_merge[col])

results_df = pd.DataFrame({
    'Column': ukb_vs_list,
    'rmse_hmean': [rmse_hmean[col] for col in ukb_vs_list],
    'r_hmea': [r_hmean[col] for col in ukb_vs_list],
    'rmse_hmax': [rmse_hmax[col] for col in ukb_vs_list],
    'r_hmax': [r_hmax[col] for col in ukb_vs_list],
})

result_file = os.path.join(main_folder, 'statistical_results', 'ukb_height.csv')
results_df.to_csv(result_file)


## plot histogram plots

fig,ax = plt.subplots(1, 1)
plot = plt.hist(gdf_oshb_merge['d_rh2_mean'], bins = np.arange(-10,10,0.5), edgecolor = "black")
ax.set_title("Histogram of Difference in Building Height")
ax.set_xlabel('OS_Building_Height - UBDC_Building_Height / m')
ax.set_ylabel('Counts')
plt.show()
fig_file = os.path.join(main_folder, 'figure', 'his_osbh_rh2_mean.jpg')
fig.savefig(fig_file, dpi=300)


fig,ax = plt.subplots(1, 1)
plot = plt.hist(gdf_ukb_merge['d_hmean_mean'], bins = np.arange(-10,10,0.5), edgecolor = "black")
ax.set_title("Histogram of Difference in Building Height")
ax.set_xlabel('UKBuilding_Height - UBDC_Building_Height / m')
ax.set_ylabel('Counts')
plt.show()
fig_file = os.path.join(main_folder, 'figure', 'his_ukb_height_mean.jpg')
fig.savefig(fig_file, dpi=300)

