import yt_dlp as youtube_dl
# Helper functions

download_directory = 'vlp/youtube-downloads'


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

