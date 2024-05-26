from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class VideoProcessingTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.video_path = 'oculus5s.mp4'
        self.upload_url = '/process-video/'

    def test_process_video(self):
        with open(self.video_path, 'rb') as video_file:
            response = self.client.post(self.upload_url, {
                'video': SimpleUploadedFile(video_file.name, video_file.read(), content_type='video/mp4'),
                'option': 'casnet2'
            })

        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())
        self.assertTrue(response.json()['success'])