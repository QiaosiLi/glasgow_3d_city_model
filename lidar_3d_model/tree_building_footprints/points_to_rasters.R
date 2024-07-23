## This script is used to generate canopy height model, treetop location, and building height model from point clouds

library(lidR)
library(raster)
library(sf)


LasToLayer <- function(las_file, output_folder)
{
  las_name <- substr(basename(las_file), 1, 6)
  print(las_name)
  
  las <- readLAS(las_file)
  if (is.empty(las)) return(NULL)
  las_t <- filter_poi(las, Classification == 5L) # select tree points
  dsm_t <- rasterize_canopy(las_t, res = 0.5, pitfree(thresholds = c(0, 10, 20), max_edge = c(0, 1.5)))
  mask_t <- pixel_metrics(las_t, ~max(Classification), res = 0.5)
  dsm_t <- mask(dsm_t, mask_t)
  dsm_t_file <- file.path(output_folder, paste0(las_name, '_50CM_DSMT.tif'))
  writeRaster(dsm_t, dsm_t_file)
  
  las_b <- filter_poi(las, Classification == 6L) # select building points
  if (is.empty(las)) return(NULL)
  dsm_b <- rasterize_canopy(las_b, res = 0.5, pitfree(thresholds = c(0, 10, 20), max_edge = c(0, 1.5)))
  mask_b <- pixel_metrics(las_b, ~max(Classification), res = 0.5)
  dsm_b <- mask(dsm_b, mask_b)
  dsm_b_file <- file.path(output_folder, paste0(las_name, '_50CM_DSMB.tif'))
  writeRaster(dsm_b, dsm_b_file)
  
  rm()
}


GridLayer <- function(output_folder, grid_name, dtm_folder){
  dtm_t_file_list <-list.files(output_folder, '*._50CM_DSMT.tif$', full.names = T)
  dtm_t_list <- lapply(dtm_t_file_list, raster)
  m_t <- do.call(merge, dtm_t_list)
  m_t_file <- file.path(output_folder, paste0(grid_name, '_50CM_DSMT.tif'))
  writeRaster(m_t, m_t_file, overwrite=TRUE)
  
  dtm_file <- file.path(dtm_folder, paste0(grid_name, '_50CM_DTM_PHASE5.tif'))
  dtm <- raster(dtm_file)
  dtm_r <- resample(dtm, m_t)
  ndsm_t <- m_t-dtm_r
  ndsm_t[ndsm_t <= 0] <- NA
  ndsm_t_file <- file.path(output_folder, paste0(grid_name, '_50CM_CHM_PHASE5.tif'))
  writeRaster(ndsm_t, ndsm_t_file, overwrite=TRUE)
  print('CHM saved')
  
  ttops <- locate_trees(ndsm_t, lmf(5))
  ttops_file <- file.path(output_folder, paste0(grid_name, '_TreeTops.shp'))
  st_write(ttops, ttops_file,layer_options = 'SHPT=POINTZ')
  print('Treetop saved')
  
  dtm_b_file_list <-list.files(output_folder, '*._50CM_NDSMB.tif$', full.names = T)
  dtm_b_list <- lapply(dtm_b_file_list, raster)
  m_b <- do.call(merge, dtm_b_list)
  ndsm_b <- m_b - dtm_r
  ndsm_b[ndsm_b <= 0] <- NA
  ndsm_b_file <- file.path(output_folder, paste0(grid_name, '_50CM_BH_PHASE5.tif'))
  writeRaster(ndsm_b, ndsm_b_file,overwrite=TRUE)
  print('BHM Saved')
  
  rm()
}


las_path <- 'data/classified_las'
output_path <- 'data/raster'
dtm_folder <- 'data/Grids/DTM/5x5km/COG-LZW'
grid_list <- c('NS56NE', 'NS46SE','NS55NW', 'NS65NE','NS66SW')
for (grid_name in grid_list) {
  print(grid_name)
  las_folder <- file.path(las_path, grid_name)
  output_folder <- file.path(output_path, grid_name)
  if (!dir.exists(output_folder)) {dir.create(output_folder)}
  
  las_file_list <-list.files(las_folder, '*._25PPM_LAS_PHASE5.las$', full.names = T)
  for (las_file in las_file_list) {
    LasToLayer(las_file,output_folder)
  }
  GridLayer(output_folder, grid_name, dtm_folder)
  gc()  
}