import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
from .utils import get_env

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotline.settings')

app = Celery('hotline',
             broker=f"amqp://{get_env('RABBITMQ_DEFAULT_USER')}:"
                    f"{get_env('RABBITMQ_DEFAULT_PASS')}@"
                    f"{get_env('RABBITMQ_HOST')}:5672/"
                    f"{get_env('RABBITMQ_DEFAULT_VHOST')}",
             backend='rpc://')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
