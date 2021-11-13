import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    imports = ("discounts_finder.celery_worker.tasks",)
    MONGO_URI = (
        f"mongodb://{os.environ['MONGO_INITDB_ROOT_USERNAME']}:{os.environ['MONGO_INITDB_ROOT_PASSWORD']}"
        f"@mongodb/{os.environ['MONGO_INITDB_DATABASE']}?authSource=admin"
    )
