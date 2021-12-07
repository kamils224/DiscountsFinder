from celery import Celery

from discounts_finder.config import Config


def make_celery():
    app = Celery(__name__, config_source=Config)
    return app


celery = make_celery()

# TODO add periodic task in future
# celery.conf.beat_schedule = {}
