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
    HUMAN_CHOICES = [
        (MULTIPLE, 'Multiple'),
        (SINGLE, 'Single'),
        (NONE, 'None'),
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