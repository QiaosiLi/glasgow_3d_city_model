# Large-scale 3D building and tree datasets constructed from airborne LiDAR point clouds in Glasgow, UK
## About this project

3D building models offer visual representation of the built environment, enabling interaction, analysis, and exploration of urban landscapes like never before. This project used large-scale high-density airborne LiDAR scanning (ALS) point clouds to produce 3D building model dataset for Glasgow City. We proposed an efficient workflow that integrated open source tool weakly supervised deep learning algorithm SQN for point cloud classification and a data-driven method City3D for 3D building reconstruction.The output includes building footprints, height attributes, building models at LoD1 and LoD2, canopy height models, tree volume, and indivual tree location.This dataset in city-wide scale and high accuracy would be a valuable source for urban environmental applications. The proposed workflow would provide a guideline for large-scale ALS data analysis from point cloud classification to 3D model construction. 

![workflow](https://github.com/user-attachments/assets/2adf8d92-950f-41d7-8b3e-28f0ef9d60aa)

The figure shows an example result of tree and building models at LoD1 ana LoD2 level.

![tree_building_model_results](https://github.com/user-attachments/assets/5c0aa859-5a9e-4893-9616-52ba6bab065d)

## Usage notes

We used Python, R, C++, CloudCompare (2.12.4), and ArcGIS Pro (3.2) to process ALS data and generate datasets. Following instruction of [SQN](https://github.com/QingyongHu/SQN?tab=readme-ov-file) to set up. SQN code for point cloud classification has been implemented with Python 3.6, TensorFlow 1.11.0, CUDA 9.0, and cuDNN 7.4.1 on Ubuntu 18.04.6. To use our [modified SQN code](https://github.com/QiaosiLi/SQN_ALS_Classification) and [annotated point cloud](https://data.ubdc.ac.uk/datasets/glasgow-3d-city-models-derived-from-airborne-lidar-point-clouds-licensed-data), and pretrain model to conduct point cloud classification. and Following [City3D](https://github.com/tudelft3d/City3D) to install and built. City3D used to construct the LoD2 building models has been implemented with Qt5 5.15.9, CGAL5.5.2, OpenCV 4.7.0, and Gurobi 10.0.1, Vision Studio 2022, 17.5.5 on Windows 10 and with Qt5 5.15.3, CGAL5.4.1, OpenCV 4.5,1 and Gurobi 11.0.0 on Ubuntu 22.04.4. This [file](https://github.com/QiaosiLi/construct_building_tree_3d_models_by_lidar/blob/master/lidar_3d_model/city3d/How%20to%20building%20City3D.md) is our step-by-step guidance to build City3D on Ubuntu 22.04.4. 
 
## Datasets
Our datasets are open in [Urban Big Data Centre data catalogue](https://data.ubdc.ac.uk/datasets/glasgow-3d-city-models-derived-from-airborne-lidar-point-clouds-open-data) and [Zenodo](https://zenodo.org/records/13273124). 
The data structure is shown in the figure below.
![lidar_remote_sensing_ql_2024](https://github.com/user-attachments/assets/460823d2-a31a-4be5-b8b6-1d288253db0a)

Note: Annotated point clouds that were prepared to train and validate point cloud classification with the SQN algorithm. The annotated point cloud data can be used to train a deep learning model for point cloud classification or as a benchmark dataset to advance point cloud manipulation.

## Citation 
If you find our work useful, please consider citing:

        @misc{https://doi.org/10.20394/vwyl2on6,
          doi = {10.20394/VWYL2ON6},
          url = {https://data.ubdc.ac.uk/dataset/8bccf530-0f07-4ff3-a8d5-443328fcd415},
          author = {{Urban Big Data Centre}},
          keywords = {Urban Planning},
          language = {en},
          title = {Glasgow 3D city models derived from airborne LiDAR point clouds licensed data},
          publisher = {University of Glasgow},
          year = {2024}
       }

## Related Repository
1. [SQN: Weakly-Supervised Semantic Segmentation of Large-Scale 3D Point Clouds](https://github.com/QingyongHu/SQN)
2. [City3D: Large-scale Building Reconstruction from Airborne LiDAR Point Clouds](https://github.com/tudelft3d/City3D)
3. [SQN_ALS_Classification](https://github.com/QiaosiLi/SQN_ALS_Classification)
