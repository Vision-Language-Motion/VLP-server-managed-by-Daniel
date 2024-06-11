import os
import yt_dlp as youtube_dl
from server.settings import BASE_DIR
from moviepy.editor import VideoFileClip

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
        for filename in os.listdir(video_directory):
            file_path = os.path.join(video_directory, filename)
            try:
                os.unlink(file_path)  # Remove the file or link
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        os.rmdir(video_directory)

    return video_directory


def get_video_file_clip(video_path):
    ''' This function returns a VideoFileClip object from the video path'''
    video = VideoFileClip(video_path)
    return video

# Screenshots
def take_screenshot_at_second(video : VideoFileClip, second, output_dir):
    """
    This function takes a screenshot of the video at a specific second and saves it to the output_path
    """
    output_path = f"{output_dir}/screenshot_at_second_{second}.png"

    video.save_frame(output_path, t=second)

    return output_path


def get_video_duration(video : VideoFileClip):
    """
    This function returns the duration of a video in seconds
    """
    return video.duration


def get_video_area(video : VideoFileClip):
    """
    This function returns the area of the video in pixels
    """
    return video.size[0] * video.size[1]