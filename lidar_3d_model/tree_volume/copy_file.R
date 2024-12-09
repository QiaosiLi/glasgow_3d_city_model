data_folder = 'C:/qll3h_2024/lidar_tree/output'
for (res in c('10m', '50m', '100m')) {
  print(res)
  raster_list = list.files(data_folder, paste0('*volume_', res, '_merge.tif$'), recursive = T, full.names = T)
  out_folder = file.path(data_folder, res)
  dir.create(out_folder)
  file.copy(raster_list, out_folder)

}

