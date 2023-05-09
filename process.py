import os
import cv2
import pyrealsense2 as rs
import numpy as np

# Create a context object
context = rs.context()

# Create a playback device and open the bag file for reading
playback_device = context.load_device_file('/home/exx/Documents/20230405_201004.bag')
playback_device.set_real_time(False)  # Optionally set playback to non-real-time mode

# Create a playback object and assign the playback device to it
playback = rs.playback(playback_device)

# Create a pipeline for processing the bag
pipeline = rs.pipeline()

# Create a config object for the pipeline
config = rs.config()

# Specify that the pipeline should process the playback object
config.enable_device(playback)

# Start the pipeline
pipeline.start(config)

# Define the directory to save the images to
output_dir = '/home/exx/Project/ws_Kowndinya/benchmarking/cdr-testing/CDR/external/realsense/images-out'

# Create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over the frames in the bag file
try:
    frame_count = 0
    while True:
        # Wait for the next frame from the bag
        frames = pipeline.wait_for_frames()

        # Convert the color and depth frames to numpy arrays
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            continue

        color_image = cv2.cvtColor(np.asanyarray(color_frame.get_data()), cv2.COLOR_RGB2BGR)
        depth_image = np.asanyarray(depth_frame.get_data())

        # Save the color and depth frames as PNG images
        color_filename = os.path.join(output_dir, f'color_{frame_count:06d}.png')
        depth_filename = os.path.join(output_dir, f'depth_{frame_count:06d}.png')

        cv2.imwrite(color_filename, color_image)
        cv2.imwrite(depth_filename, depth_image)

        frame_count += 1

except KeyboardInterrupt:
    # Stop the pipeline on keyboard interrupt
    pipeline.stop()

playback.close()
