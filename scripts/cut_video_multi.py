import cv2
import os
import numpy as np
import imageio
from PIL import Image

# Function to process a single frame
def process_frame(frame):
    # Example: Convert the frame to grayscale
    frame_rgb = frame[:,:512]
    frame_noise = frame[:,512:1024]
    
    return frame_rgb, frame_noise

# Function to read video, process frames, and write the output video
def edit_video(input_video_path, output_video_path):
    # Read the input video
    reader = imageio.get_reader(input_video_path, 'ffmpeg')
    fps = reader.get_meta_data()['fps']

    # List to store processed frames
    processed_frames = []

    for i, frame in enumerate(reader):
        if i in [0, 15, 90]:
            # Process the frame
            processed_frame_rgb, processed_frame_normal = process_frame(frame)
            
            # Save the processed frames as a image
            imageio.imwrite(f'{output_video_path[:-4]}_{i}_rgb.png', processed_frame_rgb)
            imageio.imwrite(f'{output_video_path[:-4]}_{i}_normal.png', processed_frame_normal)

    # Close the reader
    reader.close()


# Example usage
input_teaser = './assets/videos/teaser_cut'
output_teaser = './assets/videos/teaser_img'
os.makedirs(output_teaser, exist_ok=True)
for video_name in sorted(os.listdir(input_teaser)):
    input_video_path = os.path.join(input_teaser, video_name)
    output_video_path = os.path.join(output_teaser, video_name)
    if os.path.exists(f'{output_video_path[:-4]}_0_rgb.png'):
        continue
    edit_video(input_video_path, output_video_path)
