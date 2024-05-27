from celery import shared_task
from .helpers import download_video

import logging

logger = logging.getLogger(__name__)

@shared_task
def process_video_without_human(url):
    download_video(url)
    
    logger.warn(f"Processing video for URL: {url}")
    # Add your task implementation here
    
