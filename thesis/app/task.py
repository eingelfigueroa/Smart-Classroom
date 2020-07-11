from __future__ import absolute_import, unicode_literals


from celery import Celery
from celery import shared_task
from celery.decorators import task
from . import face_recog

celery = Celery('task', broker='redis://127.0.0.1:6379')
#logger = get_task_logger(__name__)
@shared_task
def printing():
    print('Im working')

@shared_task
def face_recognition():
    
    recognize = face_recog.detection

    recognize()
    logger.info("Recognition in Progress")