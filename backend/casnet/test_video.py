import os
import requests

def test_video():
    url = 'http://localhost:8000/process/process-video/'  # URL of your Django view
    video_path = 'oculus5s.mp4'  # Path to your test video

    with open(video_path, 'rb') as video_file:
        files = {'video': video_file}
        data = {'option': 'casnet2'}  # Example POST data

        response = requests.post(url, files=files, data=data)

        print('Status Code:', response.status_code)
        print('Response JSON:', response.json())

if __name__ == '__main__':
    test_video()