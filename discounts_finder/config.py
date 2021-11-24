import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    CORS_HEADERS = "Content-Type"
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
    imports = ("discounts_finder.celery_worker.tasks",)
    MONGO_URI = os.environ.get("MONGODB_URI")
