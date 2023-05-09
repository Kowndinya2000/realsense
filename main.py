import cv2
import pyrealsense2 as rs
import numpy as np
import os
# Define the directory to save the images to
output_dir = '/home/exx/Project/ws_Kowndinya/benchmarking/cdr-testing/CDR/external/realsense/images-out'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
pipe = rs.pipeline()
profile = pipe.start()
try:
  for i in range(0, 20):
    frames = pipe.wait_for_frames()
    for f in frames:
      print(f.profile)
    # Convert the color and depth frames to numpy arrays
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()

    if not color_frame or not depth_frame:
        continue

    color_image = cv2.cvtColor(np.asanyarray(color_frame.get_data()), cv2.COLOR_RGB2BGR)
    depth_image = np.asanyarray(depth_frame.get_data())

    # Save the color and depth frames as PNG images
    color_filename = os.path.join(output_dir, f'color_{i:06d}.png')
    depth_filename = os.path.join(output_dir, f'depth_{i:06d}.png')

    cv2.imwrite(color_filename, color_image)
    cv2.imwrite(depth_filename, depth_image)
finally:
    pipe.stop()
