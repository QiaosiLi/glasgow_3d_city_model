library(lidR)
library(sf)
library(raster)

## Tile 1
chm_file <- 'E:/QL_2022/LiDAR_2023/Processing/NS55NE/NS55NE_Tree_1_Chm_Rmn.tif'
chm <- raster(chm_file)
ttops <- locate_trees(chm, lmf(5))
plot(ttops)
st_write(ttops,
         'E:/QL_2022/LiDAR_2023/Processing/NS55NE/NS55NE_TreeTops.shp',
         layer_options = 'SHPT=POINTZ')


## Tile 2
chm_file <- 'E:/QL_2022/LiDAR_2023/Processing/N65NE/NS65NE_nDSM_T_Mask.tif'
chm <- raster(chm_file)
chm[chm<=0] <- NA
writeRaster(chm, 'E:/QL_2022/LiDAR_2023/Processing/N65NE/NS65NE_50CM_NDSMT.tif')
ttops <- locate_trees(chm, lmf(5))
plot(ttops)
st_write(ttops,
         'E:/QL_2022/LiDAR_2023/Processing/N65NE/N65NE_TreeTops.shp',
         layer_options = 'SHPT=POINTZ')