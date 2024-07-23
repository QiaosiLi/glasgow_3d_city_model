

Here is GitHub repository of the City3D:
[](https://github.com/tudelft3d/City3D)

Tested system: Ubuntu20.04

Installing dependencies:
Open ternimal
Update: 
sudo apt-get install
Install cmake-gui (i have cmake-gui)
cgal
[cgal installation reference (I used method 3.1):](https://doc.cgal.org/latest/Manual/usage.html)
check the cgal version offerred by package manager:
sudo apt-cache policy libcgal-dev
return:
libcgal-dev:
  Installed: 5.4-1
  Candidate: 5.4-1
  Version table:
 *** 5.4-1 500
        500 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages
        100 /var/lib/dpkg/status

I am happy with cgal v5.4, so I install it:
sudo apt-get install libcgal-dev

qt5
install qt5:
sudo apt install -y qtcreator qtbase5-dev qt5-qmake cmake
[Reference:](https://askubuntu.com/questions/1404263/how-do-you-install-qt-on-ubuntu22-04)

opencv:
sudo apt install -y g++
sudo apt install -y cmake
sudo apt install -y make
sudo apt install -y wget unzip
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.x.zip
unzip opencv.zip
mv opencv-4.x opencv
mkdir -p build && cd build
cmake ../opencv
make -j4
sudo make install
[Reference:](https://docs.opencv.org/4.x/d7/d9f/tutorial_linux_install.html)

Gurobi
[Reference:](https://www.gurobi.com/documentation/5.6/quickstart/installation_linux.html)
[Step by step video guide:](https://www.youtube.com/watch?v=OYuOKXPJ5PI)
I installed Gurobi 11.0.
After installing Gurobi and license, Gurobi library (libgurobi_c++.a) as mentioned in City3D RAEDME file.

Download the city3D source code:
git clone https://github.com/tudelft3d/City3D.git

Specifying the path to find Gurobi:
In your download code, reach 'code/cmake/FindGUROBI.cmake'
Adding your Gurobi search path after line 62
Adding your Gurobi library path after line 83
Adding your Gurobi version in like 92, for example:
find_library( GUROBI_C_LIBRARY
            NAMES gurobi100 gurobi90 gurobi95 libgurobi gurobi110
            PATHS ${SEARCH_PATHS_FOR_LIBRARIES}
            )


GitHub repository of the City3D mentions 3 options to build, and I followed the easiest way option 1 to build. 
$ cd path-to-root-dir-of-City3D
$ mkdir Release
$ cd Release
$ cmake -DCMAKE_BUILD_TYPE=Release ..
$ make
If you have your own main.cpp file, include your folder under the 'code' folder, EX:
![](E:\QL_2022\Pycharm_Test\Glasgow_Test_2023\lod2\image\C1.JPG)
Reach 'City3D/code/CMakeLists.txt', add your folder as below after line 82, and build it again.
add_subdirectory(CLI_Example_1_V2)

If you make some change in prarmeters, you also have to build it again.