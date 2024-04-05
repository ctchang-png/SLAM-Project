#!/bin/bash

sudo apt update && sudo apt upgrade

sudo apt install build-essential cmake git pkg-config libgtk-3-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev python3-dev python3-numpy \
    libtbb2 libtbb-dev libdc1394-dev

# Create the dependencies folder if it doesn't exist
mkdir -p dependencies

# Navigate into the dependencies folder
cd dependencies

# Check if Robo_Utils directory exists
if [ ! -d "Robo_Utils" ]; then
    # Clone Robo_Utils repository
    git clone https://github.com/tharp789/Robo_Utils.git
else
    echo "Robo_Utils repository already exists locally."
fi

# Check if ORB_SLAM2 directory exists
if [ ! -d "ORB_SLAM2" ]; then
    # Clone ORB_SLAM2 repository
    git clone https://github.com/raulmur/ORB_SLAM2.git
    cd ORB_SLAM2
    wget https://gist.githubusercontent.com/matlabbe/c10403c5d44af85cc3585c0e1c601a60/raw/48adf04098960d86ddf225f1a8c68af87bfcf56e/orbslam2_f2e6f51_marchnative_disabled.patch
    git apply orbslam2_f2e6f51_marchnative_disabled.patch
    cd ..
else
    echo "ORB_SLAM2 repository already exists locally."
fi

# Check if opencv directory exists
if [ ! -d "opencv" ]; then
    # Clone OpenCV repository
    git clone https://github.com/opencv/opencv.git
    cd opencv
    git checkout 3.0.0
    cd ..
else
    echo "OpenCV version 3.4.9 repository already exists locally."
fi

# Check if Pangolin directory exists
if [ ! -d "Pangolin" ]; then
    # Clone OpenCV repository
    git clone --recursive https://github.com/stevenlovegrove/Pangolin.git
    cd Pangolin
    bash scripts/install_prerequisites.sh recommended
    git checkout v0.5
    cd ..
else
    echo "Pangolin version 0.5 repository already exists locally."
fi

# Make file changes
cd ..
rsync -av "file_changes/FindFFMPEG.cmake" "dependencies/Pangolin/CMakeModules/FindFFMPEG.cmake"
rsync -av "file_changes/ffmpeg.cpp" "dependencies/Pangolin/src/video/drivers/ffmpeg.cpp"
rsync -av "file_changes/ffmpeg.h" "dependencies/Pangolin/include/pangolin/video/drivers/ffmpeg.h"
rsync -av "file_changes/display_x11.cpp" "dependencies/Pangolin/src/display/device/display_x11.cpp"
rsync -av "file_changes/System.h" "dependencies/ORB_SLAM2/include/System.h"
rsync -av "file_changes/LoopClosing.h" "dependencies/ORB_SLAM2/include/LoopClosing.h"
cd dependencies



# Make and install opencv
cd opencv
mkdir -p build && cd build
cmake ..
make -j16
sudo make install
cd ../..

# Eigen3
sudo apt install libeigen3-dev

# Make and install Pangolin
cd Pangolin
cmake -B build
cmake --build build

cd build
sudo make install
cd ../..

# ORB-SLAM2
cd ORB_SLAM2
bash build.sh
