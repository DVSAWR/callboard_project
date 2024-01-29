import os
from django.conf import settings

from celery import Celery



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'callboard_project.settings')

app = Celery('callboard_project', broker=settings.REDIS_HOST)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
