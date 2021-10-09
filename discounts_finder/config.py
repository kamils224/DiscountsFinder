import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/0'
    imports = ('discounts_finder.celery_worker.tasks',)
    MONGO_URI = 'mongodb://mongodb/discounts_finder_db'
