library(lidR)
library(raster)
library(sf)
library(rgdal)

data_folder = 'C:/qll3h_2024/lidar_tree/output'
tile_list = list.dirs(data_folder, full.names = F, recursive = F)

for (tile_name in tile_list[1]) {
  print(tile_name)
  data_path = file.path(data_folder, tile_name)
  
  if (file.exists(file.path(data_path, paste0(tile_name, '_volume_100m_merge.tif')))){
    cat('raster exisits')
    next
  }
  
  raster_file_list = list.files(data_path, '*_volume_100m.tif$', full.names = T)
  raster_list = lapply(raster_file_list, raster)
  raster_merge = do.call(merge, raster_list)
  raster_file = file.path(data_path, paste0(tile_name, '_volume_100m_merge.tif'))
  writeRaster(raster_merge, raster_file)
  
  raster_file_list = list.files(data_path, '*_volume_50m.tif$', full.names = T)
  raster_list = lapply(raster_file_list, raster)
  raster_merge = do.call(merge, raster_list)
  raster_file = file.path(data_path, paste0(tile_name, '_volume_50m_merge.tif'))
  writeRaster(raster_merge, raster_file)
  
  raster_file_list = list.files(data_path, '*_volume_10m.tif$', full.names = T)
  raster_list = lapply(raster_file_list, raster)
  raster_merge = do.call(merge, raster_list)
  raster_file = file.path(data_path, paste0(tile_name, '_volume_10m_merge.tif'))
  writeRaster(raster_merge, raster_file)
}



# data_folder = 'C:/qll3h_2024/lidar_tree/output'
# raster_list = list.files(data_folder, '*volume_100m.tif$', recursive = T, full.names = T)
# file.copy(raster_list, file.path(data_folder, 'volume_100'))


# r <- raster( file.path(out_path, paste0(tile_name, '_volume_100m_merge.tif')))
# 
# # Convert raster to polygons
# polygon_layer <- rasterToPolygons(r, na.rm = TRUE, dissolve = FALSE)
# 
# # Convert to sf object for easier handling
# sf_polygon_layer <- st_as_sf(polygon_layer)
# 
# # Plot polygons
# plot(sf_polygon_layer["value"], main = "Raster Pixels Converted to Polygons")
# 
# polygon_file = file.path(out_path, paste0(tile_name, '_volume_100m_merge.shp'))
# # Save the result to a shapefile
# st_write(sf_polygon_layer, polygon_file)
