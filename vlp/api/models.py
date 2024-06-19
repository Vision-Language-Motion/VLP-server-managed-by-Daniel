from django.db import models
from django.utils import timezone

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
        return self.url
    
class VideoTimeStamps(models.Model):
    # Store the video
    video = models.ForeignKey(URL, on_delete=models.CASCADE)

    # Store the start time
    start_time = models.FloatField()
    
    # Store the end time
    end_time = models.FloatField()

    def __str__(self):
        return self.video.url + " " + str(self.start_time) + " " + str(self.end_time)

class Keyword(models.Model):
    
    word = models.CharField(max_length=255, unique=True)
    queue_pos = models.PositiveIntegerField(unique=True)
    last_processed = models.DateTimeField(null=True, blank=True)

    def should_be_requeued(self):
        if self.last_processed is None:
            return True
        # requeue after 7 days for example
        return (timezone.now() - self.last_processed).days > 7

    def __str__(self):
        return f"{self.queue_pos}: {self.word}"
    
    def save(self, *args, **kwargs):
        if not self.last_processed:
            self.last_processed = timezone.now()  # Set current time if not set
        super(Keyword, self).save(*args, **kwargs)