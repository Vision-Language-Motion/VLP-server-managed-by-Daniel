from django.test import TestCase, Client
import os
from helpers import download_directory, download_video
from server.settings import BASE_DIR

# Create your tests here.

'''testing download_video function'''

class download_video_TestCase(TestCase):
    def setUp(self):
        # Set up a test Client
        self.client = Client()
        # Directory where files should be downloaded
        self.download_directory = os.path.join(BASE_DIR,'youtube-downloads')
        # Ensure the directory exists
        os.makedirs(self.download_directory, exist_ok=True)

    def test_directory(self):
         # Simulate a file download request
        response = self.client.get('/path/to/download/endpoint/')
        
        # Check if the response status is OK (200)
        self.assertEqual(response.status_code, 200)
        
        # Get the filename from the response headers or any other way your app specifies the filename
        filename = response['Content-Disposition'].split('filename=')[-1].strip('"')
        
        # Construct the expected file path
        file_path = os.path.join(self.download_directory, filename)
        
        # Check if the file exists in the expected directory
        self.assertTrue(os.path.exists(file_path))
    

    def tearDown(self):
         # Clean up the download directory after the test
        for filename in os.listdir(self.download_directory):
            file_path = os.path.join(self.download_directory, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
