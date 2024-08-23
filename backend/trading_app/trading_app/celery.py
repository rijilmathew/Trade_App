from __future__ import absolute_import,unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trading_app.settings")
app = Celery("celeryproject")

#we are using asia/kolkata time so we are making it False
app.conf.enable_utc=False
app.conf.update(timezone='Asia/Kolkata')

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_connection_retry_on_startup = True


app.autodiscover_tasks()

