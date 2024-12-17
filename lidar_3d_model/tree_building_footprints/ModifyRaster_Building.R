library(raster)

# raster_file <- 'E:/QL_2022/LiDAR_2023/Output_R/NS66SW/NS66SW_50CM_BH_PHASE5.tif'
# BH <- raster(raster_file)
# BH[BH <= 1] <- NA
# BH[BH >= 0] <- 1
# 
# new_folder <- 'E:/QL_2022/LiDAR_2023/Output_R/NS66SW/PostProcesssing'
# dir.create(new_folder)
# 
# out_file <- 'E:/QL_2022/LiDAR_2023/Output_R/NS66SW/PostProcesssing/NS66SW_50CM_BH_UniqueValue.tif'
# writeRaster(BH, datatype = 'INT2S', out_file, overwrite=T)


folder_path <- "E:/QL_2022/LiDAR_2023/Output_R"
output_path <- 'E:/QL_2022/LiDAR_2023/Building_Footprints'

grid_list <- list.dirs(folder_path, full.name = F, recursive = F)
grid_list_19 <- grid_list[grid_list != c('NS56NE')]
grid_list_19 <- grid_list_19[grid_list_19 != c('NS56SE')]
grid_list_19 <- grid_list_19[grid_list_19 != c('NS66NW')]
grid_list_19 <- grid_list_19[grid_list_19 != c('NS66SW')]

for (grid_name in grid_list_19) {
  print(grid_name)
  raster_file <- list.files(file.path(folder_path, grid_name),"*_50CM_BH_PHASE5.tif$", full.names = T)
  BH <- raster(raster_file)
  BH[BH <= 1] <- NA
  BH[BH >= 0] <- 1
  
  output_folder <- file.path(output_path, grid_name)
  if (!dir.exists(output_folder)) {dir.create(output_folder)}
  
  out_file <- file.path(output_folder, paste0(grid_name, '_50CM_BH_UniqueValue.tif'))
  writeRaster(BH, datatype = 'INT2S', out_file, overwrite=T)
}


