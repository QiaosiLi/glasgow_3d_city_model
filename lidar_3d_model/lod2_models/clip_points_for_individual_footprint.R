## This script is used to clip out point clouds for individual building using footprint shapefile.

library(lidR)
library(sf)
library(raster)
library(foreign)


lidar_path <- 'data/classified_las'
dbf_data <- read.dbf(dbf_file)  # table of 1km national grid shapefile 
tiles <- as.character(dbf_data$PLAN_NO) 
tiles_filename <- paste0(tiles, "_25PPM_LAS_PHASE5.las")
tiles_path <- sapply(tiles_filename, list.files, path = lidar_path, full.names = T, recursive = T) 
ctg <- readLAScatalog(tiles_path)
opt_filter(ctg) <- "-keep_class 6"  # choose building point only
shp_path <- 'data/footprint/footprints.shp'
shp <- st_read(shp_path , quiet = T)
grid_list <- c('NS56NE', 'NS56NE', 'NS66NW','NS66SW')

for (grid_name in grid_list) {
  print(grid_name)
  out_path_clip <- file.path('data/lod2', grid_name, 'building_clip')
  if (!dir.exists(out_path_clip)) {dir.create(out_path_clip)}
  opt_output_files(ctg) <- file.path(out_path_clip, '{U_ID}')
  ctg_clip <- clip_roi(ctg, shp)
  print("clipped las saved")
}
