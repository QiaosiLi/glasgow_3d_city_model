library(lidR)
library(raster)
library(sf)
library(rgdal)

data_folder = 'U:/Projects/GCC3DCityModelling/Backup_QL/LiDAR_3d_city_modelling/products/sqn_predicted_las_group_by_grid'
tile_list = list.dirs(data_folder, full.names = F, recursive = F)
# for (tile_name in tile_list){
for (tile_name in tile_list[13:23]){
  cat('5km grid:', tile_name)
  out_path = file.path('C:/qll3h_2024/lidar_tree/output', tile_name)
  if (!dir.exists(out_path)){
    dir.create(out_path)}
  else {
    print('folder exists')
    # next
  }
  
  in_path = file.path(data_folder, tile_name)
  lasfiles = list.files(in_path, '*.las$', full.names = T)
  
  i = 0
  for (las_file in lasfiles) {
    i = i+1
    cat(i ,'out of', length((lasfiles)))
    las_name = substr(basename(las_file), 1, 6)
    print(las_name)
    if (file.exists(file.path(out_path, paste0(las_name, '_volume_10m.tif')))){
      print('raster exists')
      next
    }
    las = readLAS(las_file)
    las_tree = filter_poi(las,Classification == 5L)
    if (npoints(las_tree)==0){
      'no data in las'
      next
    }
    voxels = voxel_metrics(las_tree, ~length(Z), res =0.5)
    voxels = as.data.frame(voxels)
    voxels$vol_m3 = 0.5^3
    csv_file = file.path(out_path, paste0(las_name, '_voxels_50cm.csv'))
    write.csv(voxels, csv_file)
    
    ext = extent(round(las@header@PHB$`Min X`), round(las@header@PHB$`Max X`), round(las@header@PHB$`Min Y`),round(las@header@PHB$`Max Y`))
    raster_template <- raster(ext, resolution = 10)
    raster_volume = rasterize(voxels[,c('X', 'Y')], raster_template, field = voxels$vol_m3, fun = sum)
    raster_file = file.path(out_path, paste0(las_name, '_volume_10m.tif'))
    writeRaster(raster_volume, raster_file, forma ='GTiff', overwrite = T)
    print('10m raster is saved')
    
    raster_template <- raster(ext, resolution = 50)
    raster_volume = rasterize(voxels[,c('X', 'Y')], raster_template, field = voxels$vol_m3, fun = sum)
    raster_file = file.path(out_path, paste0(las_name, '_volume_50m.tif'))
    writeRaster(raster_volume, raster_file, forma ='GTiff', overwrite = T)
    print('50m raster is saved')
    
    raster_template <- raster(ext, resolution = 100)
    raster_volume = rasterize(voxels[,c('X', 'Y')], raster_template, field = voxels$vol_m3, fun = sum)
    raster_file = file.path(out_path, paste0(las_name, '_volume_100m.tif'))
    writeRaster(raster_volume, raster_file, forma ='GTiff', overwrite = T)
    print('100m raster is saved')
    
  }
  
}



