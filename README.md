# Large-scale 3D building model datasets constructed from airborne LiDAR point clouds for Glasgow City, UK
## About this project

3D building models offer visual representation of the built environment, enabling interaction, analysis, and exploration of urban landscapes like never before. This project used large-scale high-density airborne LiDAR scanning (ALS) point clouds to produce 3D building model dataset for Glasgow City. We proposed an efficient workflow that integrated open source tool weakly supervised deep learning algorithm SQN for point cloud classification and a data-driven method City3D for 3D building reconstruction.The output includes building footprints, height attributes, building models at LoD1 and LoD2, canopy height models, and indivual tree location.This dataset in city-wide scale and high accuracy would be a valuable source for urban environmental applications. The proposed workflow would provide a guideline for large-scale ALS data analysis from point cloud classification to 3D model construction. 
![Slide5](https://github.com/user-attachments/assets/529b40c4-1fb7-4f83-8a5a-769af939f77d)

## Usage notes

We used Python, R, C++, CloudCompare (2.12.4), and ArcGIS Pro (3.2) to process ALS data and generate datasets. Please follow instruction of [SQN](https://github.com/QingyongHu/SQN?tab=readme-ov-file) to set up. SQN code for point cloud classification has been implemented with Python 3.6, TensorFlow 1.11.0, CUDA 9.0, and cuDNN 7.4.1 on Ubuntu 18.04.6. Following [City3D](https://github.com/tudelft3d/City3D) to install and built. City3D used to construct the LoD2 building models has been implemented with Qt5 5.15.9, CGAL5.5.2, OpenCV 4.7.0, and Gurobi 10.0.1, Vision Studio 2022, 17.5.5 on Windows 10 and with Qt5 5.15.3, CGAL5.4.1, OpenCV 4.5,1 and Gurobi 11.0.0 on Ubuntu 22.04.4.
 
## Datasets
Our datasets are open in [Urban Big Data Centre data catalogue](https://data.ubdc.ac.uk/datasets/glasgow-3d-city-models-derived-from-airborne-lidar-point-clouds-open-data). 

[Glasgow 3D building model data](https://data.ubdc.ac.uk/datasets/glasgow-3d-city-models-derived-from-airborne-lidar-point-clouds-open-data/resource/2198e2b3-8576-4a25-9f85-6f16bae633d4) contain building footprints with height attributes and 3D building modeling at LoD1 and LoD2 levels for Glasow City.

[Glasgow terrain data](https://data.ubdc.ac.uk/datasets/glasgow-3d-city-models-derived-from-airborne-lidar-point-clouds-open-data/resource/a0135e4b-b958-4f50-8f94-9ba881c41440) include DTM, DSM, and nDSM in 0.5 m spatial resoultion.

[Glasgow tree canopy data](https://data.ubdc.ac.uk/datasets/glasgow-3d-city-models-derived-from-airborne-lidar-point-clouds-open-data/resource/1d6ea863-7480-4eb5-a0ef-9dec329a14c8) include 0.5m CHM and treetop location.

[The annotated ALS point cloud dataset](https://data.ubdc.ac.uk/datasets/glasgow-3d-city-models-derived-from-airborne-lidar-point-clouds-licensed-data) includes the annotated point clouds that were prepared to train and validate point cloud classification with the SQN algorithm. The annotated point cloud data can be used to train a deep learning model for point cloud classification or as a benchmark dataset to advance point cloud manipulation.

## Citation 
If you find our work useful, please consider citing:
Glasgow City Council/Urban Big Data Centre (2024). Glasgow 3D city models derived from airborne LiDAR point clouds open data [Data set]. University of Glasgow. https://doi.org/10.20394/opvkevmj