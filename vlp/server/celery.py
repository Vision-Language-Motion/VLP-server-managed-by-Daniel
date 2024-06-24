from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'query-search-every-24-hours': {
        'task': 'api.tasks.query_search',
        # 'schedule': crontab(hour='*/24'),  # Runs every 24 hours
        'schedule': crontab(minute='*/1'),  # Debugging: Runs every Mintue
    },
    'process-urls-every-hour': {
        'task': 'api.tasks.process_urls',
        # 'schedule': crontab(minute=0, hour='*/1'),  # Executes every hour
        'schedule': crontab(minute='*/1'),  # Debugging: Runs every Mintue

    },
}