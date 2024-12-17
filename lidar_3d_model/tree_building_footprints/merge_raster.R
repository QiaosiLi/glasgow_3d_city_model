library(raster)

## dtm
r_folder <- 'E:/QL_2022/lidar_3d_city_modelling/original_data/Grids/DTM/5x5km/COG-LZW'
w_folder <- 'E:/QL_2022/lidar_3d_city_modelling/grids/whole_area'
r_file_list <- list.files(r_folder, '*.tif$', full.names = T)
r_list <- lapply(r_file_list, raster)
r_merge <- do.call(merge, r_list)
r_file_name <- file.path(w_folder, 'DTM_50CM.tif')
writeRaster(r_merge, r_file_name)


## ndsm building
r_folder <- 'E:/QL_2022/lidar_3d_city_modelling/building_lod1/Output_R'
w_folder <- 'E:/QL_2022/lidar_3d_city_modelling/grids/whole_area'
r_file_list <- list.files(r_folder, '*_50CM_BH_PHASE5.tif$', full.names = T, recursive = TRUE)
r_file_list2 <- r_file_list[c(1:8,10:24)]
r_list <- lapply(r_file_list2, raster)
r_merge <- do.call(merge, r_list)
r_file_name <- file.path(w_folder, 'MergeGrid23_50CM_BH.tif')
writeRaster(r_merge, r_file_name)