import logging

from celery_init import celery


@celery.task()
def hello():
    logging.warning('hello')