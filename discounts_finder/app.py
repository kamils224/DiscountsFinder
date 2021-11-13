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
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object("config.Config")

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
    "/api/discounts-finder/single-url-result/<object_id>",
    methods=["GET"],
    endpoint="single_url_result",
)
api.add_resource(
    DiscountsFinderTasksList,
    "/api/discounts-finder/discounts-tasks",
    methods=["GET"],
    endpoint="discounts_tasks",
)

if __name__ == "__main__":
    manager.run()
