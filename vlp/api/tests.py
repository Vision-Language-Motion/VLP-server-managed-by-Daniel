from django.test import TestCase, Client
import os
from helpers import download_directory, download_video
from server.settings import BASE_DIR

# Create your tests here.

'''testing download_video function'''
'''
class DownloadVideoTest(TestCase):
    def setUp(self):
        self.download_dir = 'download_directory'
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def tearDown(self):
        if os.path.exists(self.download_dir):
            for filename in os.listdir(self.download_dir):
                file_path = os.path.join(self.download_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f'Error: {e}')
            os.rmdir(self.download_dir)

    def test_download_video(self):
        url = 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
        result = download_video(url)

        # Check if the file was downloaded to the correct folder
        self.assertTrue(os.path.exists(result))
        self.assertTrue(result.endswith('.mp4'))

        # Verify file size is greater than 0 to ensure it's not empty
        self.assertGreater(os.path.getsize(result), 0)
'''