from flask import Flask
from flask_restful import Api
from flask_script import Manager
from flask_cors import CORS

from discounts_finder.api.url_processing import (
    DiscountFinderJob,
    DiscountsFinderTasksList,
)
from discounts_finder.celery_worker.celery_init import make_celery

app = Flask(__name__)
app.config.from_object("config.Config")
cors = CORS(app)

api = Api(app)

manager = Manager(app)
celery = make_celery()

api.add_resource(
    DiscountFinderJob,
    "/api/discounts-finder/process-single-url",
    methods=["POST"],
    endpoint="process_single_url",
)
api.add_resource(
    DiscountFinderJob,
    "/api/discounts-finder/discounts-tasks/<object_id>",
    methods=["GET", "DELETE"],
    endpoint="single_url_result",
)
api.add_resource(
    DiscountsFinderTasksList,
    "/api/discounts-finder/discounts-tasks",
    methods=["GET"],
    endpoint="single_url_tasks",
)

if __name__ == "__main__":
    manager.run()
