import os
import shutil

import numpy as np
from PIL import Image

def format_gascola(input_path, output_path, n=None, framerate=30):
    # Create output directories if they don't exist
    os.makedirs(output_path, exist_ok=True)

    gas_cam0 = os.path.join(input_path, "Gascola_Data", "Pose_easy_000", "cam0")
    gas_cam1 = os.path.join(input_path, "Gascola_Data", "Pose_easy_000", "cam4")

    euroc_cam0 = os.path.join(output_path, 'cam0')
    euroc_cam1 = os.path.join(output_path, 'cam1')

    os.makedirs(euroc_cam0)
    os.makedirs(euroc_cam1)

    # Left camera
    euroc_cam0_data = os.path.join(euroc_cam0, 'data')
    os.makedirs(euroc_cam0_data)
    cam0_filenames = []

    # Make cam0/data
    for filename in sorted(os.listdir(gas_cam0)):
        if filename.endswith('_pinhole.png'):
            image_num = filename.split('_')[0]
            if n and n < int(image_num):
                break
            cam0_filenames.append(filename)
            print(f"Copying {filename} from {gas_cam0} to {euroc_cam0_data}")
            shutil.copy(os.path.join(gas_cam0, filename), os.path.join(euroc_cam0_data, filename))

    # Make cam0/data.csv
    with open(os.path.join(euroc_cam0, 'data.csv'), 'w') as file:
        file.write("#timestamp [ns],filename")
        for i, filename in enumerate(cam0_filenames):
            file.write(f"{1E9 * i/framerate:f}, {filename}\n")

    # For monocular make rgb.txt
    with open(os.path.join(output_path, 'rgb.txt'), 'w') as file:
        file.write("# color images\n")
        file.write("# file: 'Gascola_Processed_Stereo_04022024'\n")
        file.write("# timestamp filename\n")
        for i,filename in enumerate(cam0_filenames):
            file.write(f"{i/framerate:f} {os.path.join('cam0', 'data', filename)}\n")

    # Right camera
    euroc_cam1_data = os.path.join(euroc_cam1, 'data')
    os.makedirs(euroc_cam1_data)
    cam1_filenames = []
    
    # Make cam1/data
    for filename in sorted(os.listdir(gas_cam1)):
        if filename.endswith('_pinhole.png'):
            image_num = filename.split('_')[0]
            if n and n < int(image_num):
                break
            cam1_filenames.append(filename)
            print(f"Copying {filename} from {gas_cam1} to {euroc_cam1_data}")
            shutil.copy(os.path.join(gas_cam1, filename), os.path.join(euroc_cam1_data, filename))

    # Make cam1/data.csv
    with open(os.path.join(euroc_cam0, 'data.csv'), 'w') as file:
        file.write("#timestamp [ns],filename\n")
        for i, filename in enumerate(cam1_filenames):
            file.write(f"{int(1E9 * i/framerate)}, {filename}\n")

    # Make EuRoC timestamps
    with open(os.path.join(output_path, "EuRoC_timestamps.txt"), 'w') as file:
        # Take the longest string of files, but I think it breaks if there's mismatch that occurs
        filenames = cam0_filenames if len(cam0_filenames) > len(cam1_filenames) else cam1_filenames
        for i, filename in enumerate(filenames):
            file.write(f"{filename.split('.')[0]}\n")
            #file.write(f"{int(1E9 * i/framerate)}\n")


def gascola_to_RGBD_TUM(input_path, output_path, framerate=30, use_depth_gt=False, depth_scalar=70.0):
    """
    Reformat the gascola data into the TUM RGB-D expected layout

    Gascola/
    |-camera_intrinsics.txt
    |-camera_poses.txt
    |-all_poses.npy
    |-rgb/
    | |-000000_pinhole.png
    |-depth_estimated/
    | |-000000_pinhole.png
    |-depth_ground_truth/
    | |-000000_pinhole.png



    TUM Dataset/
    |-accelerometer.txt
    |-depth.txt             # csv mapping timestamps to rgb image paths
    |-groundtruth.txt
    |-rgb.txt               # csv mapping timestamps to depth image paths
    |-associations.txt # from scripts.associate.py
    |-depth/
    | |-xxx.png # depth (greyscale of some kind)
    |-rgb/
    | |-xxx.png # rgb
    """
    # collect image paths
    rgb_imgs = []
    depth_est_arrs = []
    depth_gt_arrs = []

    for root, dirs, files in os.walk(input_path):
        for file in files:
            file_path = os.path.join(file)
            if "rgb" in root:
                rgb_imgs.append(file_path)
            if "depth_estimated" in root:
                depth_est_arrs.append(file_path)
            if "depth_ground_truth" in root:
                depth_gt_arrs.append(file_path)

    # Make in order
    rgb_imgs.sort(key=lambda filename: int(filename.split('_')[0]))
    depth_est_arrs.sort(key=lambda filename: int(filename.split('_')[0]))
    depth_gt_arrs.sort(key=lambda filename: int(filename.split('_')[0]))

    # Create output dataset dir
    try:
        os.makedirs(output_path)
        print(f"Created new dataset in {output_path}")
    except FileExistsError:
        print(f"{output_path} already exists")

    # Make rgb/
    try:
        os.makedirs(os.path.join(output_path, "rgb"))
    except FileExistsError:
        print(f"{output_path}/rgb already exists")

    # Make rgb.txt and rgb/*
    with open(os.path.join(output_path, "rgb.txt"), 'w') as file:
        print(f"Creating {output_path}/rgb.txt")
        file.write("# rgb maps\n")
        file.write("# file: 'Project Data/Sim Data (google drive)'\n")
        file.write("# timestamp filename\n")

        for i, rgb_img in enumerate(rgb_imgs):
            t = i/framerate
            file.write(f"{t} rgb/{rgb_img}\n")

            src = os.path.join(input_path, "rgb", rgb_img)
            dst = os.path.join(output_path, "rgb", rgb_img)
            shutil.copyfile(src, dst)
            print(f"Copying {src} to {dst}")

    # Make depth/
    try:
        os.makedirs(os.path.join(output_path, "depth"))
    except FileExistsError:
        print(f"{output_path}/depth already exists")

    # Make depth.txt
    with open(os.path.join(output_path, "depth.txt"), 'w') as file:
        print(f"Creating {output_path}/depth.txt")
        file.write("# depth maps\n")
        file.write("# file: 'Project Data/Sim Data (google drive)'\n")
        file.write("# timestamp filename\n")

        if use_depth_gt:
            depth_arrs = depth_gt_arrs
        else:
            depth_arrs = depth_est_arrs

        depth_max = 0
        for i, depth_arr in enumerate(depth_arrs):
            depth_img = depth_arr.split('.')[0] + '.png'

            t = i/framerate
            file.write(f"{t} depth/{depth_img}\n")

            # Load numpy data
            print(f"Reading depth file {depth_arr}")
            if use_depth_gt:
                src = os.path.join(input_path, "depth_ground_truth", depth_arr)
            else:
                src = os.path.join(input_path, "depth_estimated", depth_arr)

            depth_np = np.load(src)
            depth_max = max(np.max(depth_np), depth_max)
            # Convert to depth image
            print(f"Converting from numpy array to depth image")

            depth_np_uint8 = (depth_np * (255 / depth_scalar)).astype(np.uint8)
            depth_PIL = Image.fromarray(depth_np_uint8)
            
            # Save depth image
            dst = os.path.join(output_path, "depth", depth_img)
            depth_PIL.save(dst)

            print(f"Saving depth data from {src} image at {dst}")



    print(f"Depth max: {depth_max}")

def real_world_to_RGBD_TUM(input_path, output_path, framerate=30, depth_scalar=30.0):
    """
    Reformat the gascola data into the TUM RGB-D expected layout

    Gascola/
    |-camera_intrinsics.txt
    |-camera_poses.txt
    |-all_poses.npy
    |-rgb/
    | |-000000_pinhole.png
    |-depth_estimated/
    | |-000000_pinhole.png
    |-depth_ground_truth/
    | |-000000_pinhole.png



    TUM Dataset/
    |-accelerometer.txt
    |-depth.txt             # csv mapping timestamps to rgb image paths
    |-groundtruth.txt
    |-rgb.txt               # csv mapping timestamps to depth image paths
    |-associations.txt # from scripts.associate.py
    |-depth/
    | |-xxx.png # depth (greyscale of some kind)
    |-rgb/
    | |-xxx.png # rgb
    """
    # collect image paths
    rgb_imgs = []
    depth_arrs = []

    for root, dirs, files in os.walk(input_path):
        for file in files:
            file_path = os.path.join(file)
            if "rgb" in root:
                rgb_imgs.append(file_path)
            if "depth_processed" in root:
                depth_arrs.append(file_path)

    # Make in order
    rgb_imgs.sort(key=lambda filename: int(filename.split('_')[0]))
    depth_arrs.sort(key=lambda filename: int(filename.split('_')[0]))

    # Create output dataset dir
    try:
        os.makedirs(output_path)
        print(f"Created new dataset in {output_path}")
    except FileExistsError:
        print(f"{output_path} already exists")

    # Make rgb/
    try:
        os.makedirs(os.path.join(output_path, "rgb"))
    except FileExistsError:
        print(f"{output_path}/rgb already exists")

    # Make rgb.txt and rgb/*
    with open(os.path.join(output_path, "rgb.txt"), 'w') as file:
        print(f"Creating {output_path}/rgb.txt")
        file.write("# rgb maps\n")
        file.write("# file: 'Project Data/Sim Data (google drive)'\n")
        file.write("# timestamp filename\n")

        for i, rgb_img in enumerate(rgb_imgs):
            t = i/framerate
            file.write(f"{t} rgb/{rgb_img}\n")

            src = os.path.join(input_path, "rgb", rgb_img)
            dst = os.path.join(output_path, "rgb", rgb_img)
            shutil.copyfile(src, dst)
            print(f"Copying {src} to {dst}")

    # Make depth/
    try:
        os.makedirs(os.path.join(output_path, "depth"))
    except FileExistsError:
        print(f"{output_path}/depth already exists")

    # Make depth.txt
    with open(os.path.join(output_path, "depth.txt"), 'w') as file:
        print(f"Creating {output_path}/depth.txt")
        file.write("# depth maps\n")
        file.write("# file: 'Project Data/Sim Data (google drive)'\n")
        file.write("# timestamp filename\n")

        depth_max = 0
        for i, depth_arr in enumerate(depth_arrs):
            depth_img = depth_arr.split('.')[0] + '.png'

            t = i/framerate
            file.write(f"{t} depth/{depth_img}\n")

            # Load numpy data
            print(f"Reading depth file {depth_arr}")
            src = os.path.join(input_path, "depth_processed", depth_arr)

            depth_np = np.load(src)
            # clip infinite values
            depth_np[depth_np > 1E5] = 0
            depth_max = max(np.max(depth_np), depth_max)
            # Convert to depth image
            print(f"Converting from numpy array to depth image")

            depth_np_uint8 = (depth_np * (255 / depth_scalar)).astype(np.uint8)
            depth_PIL = Image.fromarray(depth_np_uint8)
            
            # Save depth image
            dst = os.path.join(output_path, "depth", depth_img)
            depth_PIL.save(dst)

            print(f"Saving depth data from {src} image at {dst}")



    print(f"Depth max: {depth_max}")


if __name__ == "__main__":
    # input_path = "data/Gascola"
    # output_path = "data/Gascola_RGBD_TUM"

    input_path = "data/Real_World"
    output_path = "data/Real_World_RGB_TUM"

    real_world_to_RGBD_TUM(input_path, output_path)
    print("Dataset reformatting completed.")
