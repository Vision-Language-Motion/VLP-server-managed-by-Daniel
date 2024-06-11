from django.test import TestCase, Client
import os
from .helpers import download_directory, download_video, delete_file
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

'''testing delete function'''
class DeleteTest(TestCase):
    def test_delete_file(self):
        '''Testing the delete_file function by downloading a video deleting the file 
           and checking if it exists afterwards'''
        # Creating test file
        file_path = download_video('https://www.youtube.com/shorts/AsrP4ji_Dtw')
        
        # Delete the file
        delete_file(file_path)

        # Checking if the file exists
        assert(not (os.path.exists(file_path)))

'''testing Create Folder function'''
    
'''testing Delete Folder function'''