import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firma_v02.settings')

app = Celery('firma_v02')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
