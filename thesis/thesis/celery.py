from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from celery._state import _set_current_app
import django

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thesis.settings')
app = Celery('thesis')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'meme': {
        'task': 'app.task.printing',
        'schedule': crontab()
        
    },

    'face-recognition': {
        'task': 'app.task.face_recognition',
        'schedule': crontab(minute=15)
    }
}

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
