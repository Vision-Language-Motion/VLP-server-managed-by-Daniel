from celery import shared_task
from .helpers import download_video, delete_file, create_folder_from_video_path, delete_folder_from_video_path, \
                    take_screenshot_at_second


import logging

logger = logging.getLogger(__name__)

@shared_task
def process_video_without_human(url):
    
    logger.warn(f"Processing video for URL: {url}")
    

    file_path = download_video(url)
    create_folder_from_video_path(file_path)
    take_screenshot_at_second(file_path, 1, )
    # delete(file_path)
    
