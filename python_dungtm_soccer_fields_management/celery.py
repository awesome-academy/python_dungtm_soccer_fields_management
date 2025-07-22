# project_name/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_dungtm_soccer_fields_management.settings')

app = Celery('python_dungtm_soccer_fields_management')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
