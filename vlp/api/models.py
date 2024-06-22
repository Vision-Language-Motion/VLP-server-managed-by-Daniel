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
    last_processed = models.DateTimeField(null=True, blank=True)
    use_counter = models.PositiveIntegerField(default=0)
    quality_metric = models.DecimalField(default = 0, decimal_places=4, max_digits=8)
    

    def __str__(self):
        return f"{self.word}: {self.last_processed} :{self.use_counter}"


    def update_used_keyword(self, count=0):
        self.use_counter += count
        self.last_processed = timezone.now()
        self.save(update_fields=['use_counter', 'last_processed'])

    
    def save(self, *args, **kwargs):
        if not self.last_processed:
            self.last_processed = timezone.now() - timezone.now()  # Set to time 0 if not set
        super(Keyword, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-last_processed', 'use_counter']
