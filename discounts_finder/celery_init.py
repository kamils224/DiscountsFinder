import logging

from celery import Celery

from config import Config


def make_celery():
    app = Celery(__name__, broker=Config.CELERY_BROKER_URL)
    app.config_from_object(Config)
    return app


celery = make_celery()

celery.conf.beat_schedule = {
}
