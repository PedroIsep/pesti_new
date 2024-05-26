from moviepy.editor import VideoFileClip
import os
import sys

def extract_frames(clip, times, frames_dir):
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    
    for t in times:
        video_path = os.path.join(frames_dir, '{:05d}.jpg'.format(int(t*clip.fps)))
        clip.save_frame(video_path, t)

if __name__ == "__main__":
    video_path = sys.argv[1]
    frames_dir = sys.argv[2]
    
    clip = VideoFileClip(video_path)
    times = [i for i in range(0, int(clip.duration * 2))]  # 2 frames per second
    times = [t / 2.0 for t in times]  # Convert frame numbers to seconds
    
    extract_frames(clip, times, frames_dir)