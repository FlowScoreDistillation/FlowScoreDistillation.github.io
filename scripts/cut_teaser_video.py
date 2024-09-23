import cv2
import os
import numpy as np
import imageio
from PIL import Image
# Function to process a single frame
def process_frame(frame):
    # Example: Convert the frame to grayscale
    frame_rgb = frame[:,:512]
    frame_noise = frame[:,512*2:512*3]
    processed_frame = np.concatenate((frame_rgb, frame_noise), axis=1)
    return processed_frame

def process_frame_composite(frame):
    # Example: Convert the frame to grayscale
    frame_rgb = frame[:,:512]
    frame_noise = frame[:,512*2:512*3]
    
    # # Convert frame_noise to a Pillow Image
    # noise_img = Image.fromarray(frame_noise)

    # # Resize noise frame to 0.25 of its original size
    # new_size = (noise_img.width // 4, noise_img.height // 4)
    # resized_noise_img = noise_img.resize(new_size, Image.ANTIALIAS)

    # # Convert the resized noise image back to a NumPy array
    # resized_frame_noise = np.array(resized_noise_img)
        
    # # put noise frame on right bottom
    # frame_rgb[-resized_frame_noise.shape[0]:, -resized_frame_noise.shape[1]:] = resized_frame_noise
    return frame_rgb


# Function to read video, process frames, and write the output video
def edit_video(input_video_path, output_video_path):
    # Read the input video
    reader = imageio.get_reader(input_video_path, 'ffmpeg')
    fps = reader.get_meta_data()['fps']

    # List to store processed frames
    processed_frames = []

    for frame in reader:
        # Process the frame
        processed_frame = process_frame(frame)

        # Append the processed frame to the list
        processed_frames.append(processed_frame)

    # Close the reader
    reader.close()

    # Save the processed frames as a new video
    imageio.mimsave(output_video_path, processed_frames, fps=fps)

def composite_edit_video(input_video_path_0, input_video_path_1, input_video_path_2, input_video_path_3, output_video_path):
    # Read the input video
    reader_0 = imageio.get_reader(input_video_path_0, 'ffmpeg')
    reader_1 = imageio.get_reader(input_video_path_1, 'ffmpeg')
    reader_2 = imageio.get_reader(input_video_path_2, 'ffmpeg')
    
    reader_3 = imageio.get_reader(input_video_path_3, 'ffmpeg')
    
    fps = reader_0.get_meta_data()['fps']

    # List to store processed frames
    processed_frames = []

    for frame_0, frame_1, frame_2, frame_3 in zip(reader_0, reader_1, reader_2, reader_3):
        # Process the frame
        processed_frame_0 = process_frame_composite(frame_0)
        processed_frame_1 = process_frame_composite(frame_1)
        processed_frame_2 = process_frame_composite(frame_2)
        processed_frame_3 = process_frame_composite(frame_3)
        processed_frame = np.concatenate((processed_frame_0, processed_frame_1, processed_frame_2, processed_frame_3), axis=1)
        
        # append
        processed_frames.append(processed_frame)
        
        # close the reader
    reader_0.close()
    reader_1.close()
    reader_2.close()
    reader_3.close()
    
    # Save the processed frames as a new video
    imageio.mimsave(output_video_path, processed_frames, fps=fps)
        
    
# Example usage
input_teaser = './assets/videos/teaser'
output_teaser = './assets/videos/teaser_cut'
os.makedirs(output_teaser, exist_ok=True)
for video_name in sorted(os.listdir(input_teaser)):
    input_video_path = os.path.join(input_teaser, video_name)
    output_video_path = os.path.join(output_teaser, video_name)
    if os.path.exists(output_video_path):
        continue
    edit_video(input_video_path, output_video_path)

for video_name in sorted(os.listdir(input_teaser)):
    if video_name[-5] == '0':
        video_name_1 = video_name[:-5] + '1.mp4'
        video_name_2 = video_name[:-5] + '2.mp4'
        video_name_3 = video_name[:-5] + '3.mp4'
        composite_video_name = video_name[:-5] + 'composite.mp4'
        input_video_path_0 = os.path.join(input_teaser, video_name)
        input_video_path_1 = os.path.join(input_teaser, video_name_1)
        input_video_path_2 = os.path.join(input_teaser, video_name_2)
        input_video_path_3 = os.path.join(input_teaser, video_name_3)
        if os.path.exists(input_video_path_1) and os.path.exists(input_video_path_2) and os.path.exists(input_video_path_3):
            output_video_path = os.path.join(output_teaser, composite_video_name)
            print(composite_video_name)
            # if os.path.exists(output_video_path):
            #     continue
            composite_edit_video(input_video_path_0, input_video_path_1, input_video_path_2, input_video_path_3, output_video_path)