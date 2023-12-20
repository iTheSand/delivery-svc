"""Celery initialization"""

import os

from celery import Celery
from django.conf import settings  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "delivery.settings")
app = Celery("main")
app.conf.task_acks_late = True

app.config_from_object("django.conf:settings")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "cache-usd-exchange-rate": {
        "task": "apps.core.tasks.cache_usd_exchange_rate", "schedule": 60 * 60 * 6
    },
}
