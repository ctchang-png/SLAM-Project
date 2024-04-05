# SLAM-Project
# -data/
# --Gascola_Processed_Stereo_04022024
# --Gascola_Formatted
# -- Other TUMX or EuRoC sets
# -dependencies/
# --opencv/
# --ORB_SLAM2/
# --Pangolin/
# --Robo_Utils/
# -scripts/
# --format_data.py (format the zipped Gascola_Processed_Stereo_04022024 dataset into TUM and EuRoC formats)


# Run from ORB_SLAM2
# Stereo
./Examples/Stereo/stereo_euroc Vocabulary/ORBvoc.txt Examples/Stereo/EuRoC.yaml ../../data/Gascola_Formatted/cam0/data ../../data/Gascola_Formatted/cam1/data ../../data/Gascola_Formatted/EuRoC_timestamps.txt 
# Monocular
./Examples/Monocular/mono_tum Vocabulary/ORBvoc.txt Examples/Monocular/TUM1.yaml ../../data/Gascola_Formatted/
