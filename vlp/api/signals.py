# signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Video
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
        logger.warn("Loading task")
        
        from .tasks import process_video_without_human
        timestamps, preds = process_video_without_human(instance.url)
        pred = preds[0]

        if pred["overall_prediction"] == "multiple":
            instance.human_presence = Video.MULTIPLE
        elif pred["overall_prediction"] == "single":
            instance.human_presence = Video.SINGLE
            if pred["quality"] == "high":
                instance.visibility = Video.HIGH
            elif pred["quality"] == "medium":
                instance.visibility = Video.MEDIUM
            else:
                instance.visibility = Video.LOW

        # task_id = process_video_without_human.delay(instance.url) delaying does not work with poseestimator
        instance._processed_by_signal = True  # Setze das Flag, um erneute Verarbeitung zu verhindern


