import os
from PIL import Image
import cv2
import sys

# Get the current working directory
current_path = os.getcwd()

# Folder containing images
img_dir = './processed_frames'

#Generate a video from all images in the specified folder.
def create_video_from_images(folder):
    video_filename = 'created_video.mp4'
    valid_images = [i for i in os.listdir(folder) if i.endswith((".jpg", ".jpeg", ".png"))]

    first_image = cv2.imread(os.path.join(folder, valid_images[0]))
    h, w, _ = first_image.shape

    codec = cv2.VideoWriter_fourcc(*'avc1')
    vid_writer = cv2.VideoWriter(video_filename, codec, 30, (w, h))

    for img in valid_images:
        loaded_img = cv2.imread(os.path.join(folder, img))
        for _ in range(20):
            vid_writer.write(loaded_img)

    vid_writer.release()

    
if __name__ == "__main__":
    img_dir = sys.argv[1]
    create_video_from_images(img_dir)
