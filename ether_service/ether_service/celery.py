from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import logging

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ether_service.settings')
app = Celery('ether_service')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
logger.info("Celery started successfully")


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
