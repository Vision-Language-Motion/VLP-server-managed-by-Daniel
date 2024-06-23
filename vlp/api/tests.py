from django.test import TestCase, Client
import os
from .helpers import download_directory, download_video, delete_file, add_Url_to_db, add_keyword_to_Query
from server.settings import BASE_DIR
from .tasks import process_video_without_human, query_search
from .models import URL, Query
from datetime import datetime


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

''''
class PysceneTest(TestCase):
    """Test the process_video_without_human function from tasks.py with the
       new pyscene implementation."""

    def test_pyscene(self):
        video_url = 'https://www.youtube.com/shorts/AsrP4ji_Dtw'
        timestamps, preds = process_video_without_human(video_url)
        assert(len(preds) == len(timestamps))
        assert(len(preds) > 0)
'''

class AddUrlToDB(TestCase):
    """Test the add_Url_to_db by adding a Url to the URL model and then checking if it exists"""
    
    def test_add_Url_to_db(self):
        video_url = 'https://www.youtube.com/shorts/AsrP4ji_Dtw'
        add_Url_to_db(video_url)
        assert(URL.objects.filter(url= video_url).exists())


class AddKeywordQuery(TestCase):
    """Test the add_Keyword_to_Query by adding a keyword to the Query model and then checking if it exists"""
    
    def test_add_Keyword_to_Query(self):
        keyword = 'workout'
        add_keyword_to_Query(keyword)
        assert(Query.objects.filter(keyword=keyword).exists())

class AddKeywordDuplicate(TestCase):
    """Test the add_keyword_to_Query by adding a keyword twice to the Query model and then checking if only one exists"""
    
    def test_add_duplicate_keyword_to_query(self):
        """Test that adding a keyword in different cases and with whitespace results in a single entry."""

        # Define the keywords
        keyword_with_trailing_space = 'workout '
        keyword_capitalized = 'Workout'

        # Add the first keyword
        add_keyword_to_Query(keyword_with_trailing_space)

        try:
            # try adding the second keyword
            add_keyword_to_Query(keyword_capitalized)
        except:
            pass

        # Check the database for the cleaned keyword
        cleaned_keyword = 'workout'
        query_count = Query.objects.filter(keyword=cleaned_keyword).count()

        # Assert that only one entry exists
        self.assertEqual(query_count, 1)

class QuerySearch(TestCase):
    def test_query_search(self):
        query_search()
