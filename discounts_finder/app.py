from flask import Flask
from flask_restful import Api
from flask_script import Manager

from discounts_finder.api.url_processing import DiscountFinderJob
from discounts_finder.celery_worker.celery_init import make_celery

app = Flask(__name__)
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

if __name__ == "__main__":
    manager.run()
