# signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Video
from .tasks import process_video_without_human
import logging

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Video)
def check_video_conditions(sender, instance, **kwargs):
    if instance._processed_by_signal:
        return
    
    logger.warn(f"Human presence {instance.human_presence}")

    # human_presence is optional, check if it is set
    if not instance.human_presence and ('youtube.com' in instance.url or 'youtu.be' in instance.url):
        logger.warn(f"Scheduling Task for Human presence {instance.human_presence}")

        # edit the instance to have a ? as human presence until checked
        instance.human_presence = Video.UNKNOWN
        task_id = process_video_without_human.delay(instance.url)
        instance._processed_by_signal = True  # Setze das Flag, um erneute Verarbeitung zu verhindern


