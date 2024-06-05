import os
import yt_dlp as youtube_dl
from server.settings import BASE_DIR
from moviepy.editor import VideoFileClip

# Helper functions

# Definining download directory
download_directory = os.path.join(BASE_DIR,'youtube-downloads')

# Download
def download_video(url):
    """
    This function creates a variable ydl_opts containing how the video should be downloaded 
    and then uses the yt_dlp module to download the video into the download_directory
    """
    ydl_opts = {
        'format': 'best[height<=720]',  # best quality up to 720p
        'outtmpl': f'{download_directory}/%(id)s.%(ext)s',  # Save file as the video ID
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  # Ensure the video is in mp4 format
        }]
    }

    # Create a YoutubeDL object with the options
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    video_id = youtube_dl.YoutubeDL().extract_info(url, download=False)['id']
    file_path = f"{download_directory}/{video_id}.mp4"
    return file_path


# Delete 
def delete_file(file_path):
    ''' This function checks if a file (/the directory) exists and deletes it'''
    if os.path.exists(file_path):
        os.remove(file_path)

    return file_path

# Create/Delete Folder
def create_folder_from_video_path(video_path):
    ''' This function creates a folder from the video path'''
    video_id = video_path.split('.')[0]
    new_video_directory = os.path.join(BASE_DIR, video_id)  # Create a new directory for the video screenshots

    if not os.path.exists(new_video_directory):
        os.makedirs(new_video_directory)

    return new_video_directory


def delete_folder_from_video_path(video_path):
    ''' This function deletes a folder from the video path'''
    video_id = video_path.split('.')[0]
    video_directory = os.path.join(BASE_DIR, video_id)

    if os.path.exists(video_directory):
        os.rmdir(video_directory)

    return video_directory

# Screenshots
def take_screenshot_at_second(video_path, second, output_path):
    """
    This function takes a screenshot of the video at a specific second and saves it to the output_path
    """
    
    video = VideoFileClip(video_path)
    screenshot = video.get_frame(second)
    screenshot.save_frame(output_path)

    return output_path