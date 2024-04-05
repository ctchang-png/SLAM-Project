import os
import shutil

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





if __name__ == "__main__":
    input_path = "data/Gascola_Processed_Stereo_04022024"
    output_path = "data/Gascola_Formatted"

    format_gascola(input_path, output_path, n=500)
    print("Dataset reformatting completed.")
