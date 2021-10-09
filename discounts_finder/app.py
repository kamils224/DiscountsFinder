from flask import Flask
from flask_restful import Api
from flask_script import Manager

from discounts_finder.api.url_processing import DiscountFinderJob
from discounts_finder.celery_worker.celery_init import make_celery
from discounts_finder.mongo import mongo

app = Flask(__name__)
app.config.from_object("config.Config")

api = Api(app)
mongo.init_app(app)

manager = Manager(app)
celery = make_celery()

api.add_resource(DiscountFinderJob, "/api/add-discounts-finder-job")

if __name__ == "__main__":
    manager.run()
