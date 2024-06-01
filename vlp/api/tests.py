from django.test import TestCase, Client
import os
from .helpers import download_directory, download_video
from server.settings import BASE_DIR

# Create your tests here.

'''testing download_video function'''

class DownloadVideoTest(TestCase):
    def test_video_download(self):
        '''Testing the download_video function by downloading a video 
           and then checking if it exist in the download directory '''
        #The video we are using for this Test 
        video_url = 'https://www.youtube.com/shorts/AsrP4ji_Dtw'
    
        # Download the video
        video_path = download_video(video_url)

        # Check if the file exists in the download directory
        assert(os.path.exists(video_path))
