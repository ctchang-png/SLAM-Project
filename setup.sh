#!/bin/bash

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
else
    echo "ORB_SLAM2 repository already exists locally."
fi