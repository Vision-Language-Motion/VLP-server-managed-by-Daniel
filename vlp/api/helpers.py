import os
import yt_dlp as youtube_dl
from server.settings import BASE_DIR
import logging

# Helper functions

# Definining download directory
download_directory = os.path.join(BASE_DIR,'youtube-downloads')

# Download
def download_video(url):
    """
    Downloads a video from the given URL using yt_dlp and saves it to the specified directory.

    Args:
        url (str): The URL of the video to download.

    Returns:
        str: The file path of the downloaded video, or None if the download failed.
    """
    ydl_opts = {
        'format': 'best[height<=720]',  # best quality up to 720p
        'outtmpl': f'{download_directory}/%(id)s.%(ext)s',  # Save file as the video ID
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  # Ensure the video is in mp4 format
        }]
    }

    try:
        # Create a YoutubeDL object with the options and download the video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Extract video ID and construct file path
        video_info = youtube_dl.YoutubeDL().extract_info(url, download=False)
        video_id = video_info['id']
        file_path = f"{download_directory}/{video_id}.mp4"
        
        logging.info(f'Video downloaded successfully: {file_path}')
        return file_path
    except youtube_dl.utils.DownloadError as e:
        logging.error(f'Error downloading video: {e}')
    except Exception as e:
        logging.error(f'An unexpected error occurred: {e}')
    

    return None


# Delete 
def delete(file_path):
    ''' This function checks if a file (/the directory) exists and deletes it'''
    try:
        if (os.path.exists(file_path)):
            os.remove(file_path)
            logging.info(f'File deleted successfully: {file_path}')
            return
    except Exception as e:
        logging.error(f'Error occurred while deleting file {file_path}: {e}')
 
    logging.error(f'File: {file_path}, does not exist')
    return
    