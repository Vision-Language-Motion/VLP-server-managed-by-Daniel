import os
import yt_dlp as youtube_dl
from server.settings import BASE_DIR

# Helper functions

# Definining download directory
download_directory = os.path.join(BASE_DIR,'youtube-downloads')


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



   



def delete(file):
    ''' This function checks if a file (/the directory) exists and deletes it'''
    if (os.path.exists(file)):
        os.remove(file)
        return
 
    print (f'File: {file}, does not exist')
    return
    