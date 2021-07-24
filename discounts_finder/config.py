import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_IMPORTS = ('discounts_finder.tasks',)
    MONGO_URI = 'mongodb://mongodb/discounts_finder_db'
