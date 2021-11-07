from flask import Flask
from flask_restful import Api
from flask_script import Manager
from flask_cors import CORS, cross_origin

from discounts_finder.api.url_processing import DiscountFinderJob, DiscountsFinderTasksList
from discounts_finder.celery_worker.celery_init import make_celery

app = Flask(__name__)
CORS(app)
app.config.from_object("config.Config")

api = Api(app)

manager = Manager(app)
celery = make_celery()

api.add_resource(DiscountFinderJob, "/api/discounts-finder/process-single-url", methods=["POST"],
                 endpoint="process_single_url")
api.add_resource(DiscountFinderJob, "/api/discounts-finder/single-url-result/<object_id>", methods=["GET"],
                 endpoint="single_url_result_details")
api.add_resource(DiscountsFinderTasksList, "/api/discounts-finder/single-url-result", methods=["GET"],
                 endpoint="single_url_result_list")

if __name__ == "__main__":
    manager.run()
