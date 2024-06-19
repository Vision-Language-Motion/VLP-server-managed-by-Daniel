from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'requeue-keywords-every-48-hours': {
        'task': 'server.tasks.cycle_keywords',
        'schedule': crontab(hour='*/48'),  # Run every 48 hours
    },
}