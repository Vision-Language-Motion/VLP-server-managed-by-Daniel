from django.db import models

class Video(models.Model):
    # Store the YouTube URL
    url = models.URLField()

    # store the keywords, used to search fo the video
    keywords = models.TextField(blank=True, null=True)

    # Choices for the presence of humans
    MULTIPLE = 'M'
    SINGLE = 'S'
    NONE = '-'
    UNKNOWN = '?'
    HUMAN_CHOICES = [
        (MULTIPLE, 'Multiple'),
        (SINGLE, 'Single'),
        (NONE, 'None'),
        (UNKNOWN, 'Unknown'),
    ]
    human_presence = models.CharField(max_length=1, choices=HUMAN_CHOICES, blank=True, null=True)

    # Choices for visibility level when only one human is present
    HIGH = 'HI'
    MEDIUM = 'ME'
    LOW = 'LO'
    VISIBILITY_CHOICES = [
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    ]
    visibility = models.CharField(max_length=2, choices=VISIBILITY_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.url
    
    def __init__(self, *args, **kwargs):
        super(Video, self).__init__(*args, **kwargs)
        self._processed_by_signal = False


class URL(models.Model):
    # Store the URL
    url = models.URLField(unique=True)

    is_processed = models.BooleanField(default=False)


    def __str__(self):
        return self.url + " " + str(self.is_processed) + " " + str(self.id)
    
class VideoTimeStamps(models.Model):
    # Store the video
    video = models.ForeignKey(URL, on_delete=models.CASCADE)

    # Store the start time
    start_time = models.FloatField()
    
    # Store the end time
    end_time = models.FloatField()

    def __str__(self):
        return self.video.url + " " + str(self.start_time) + " " + str(self.end_time)
    
class Prediction(models.Model):
    video_timestamp = models.ForeignKey(VideoTimeStamps, on_delete=models.CASCADE)

    prediction = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return self.video_timestamp.video.url + " " + str(self.video_timestamp.start_time) + " " + str(self.video_timestamp.end_time) + " " + self.prediction