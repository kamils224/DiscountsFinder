from flask import Flask
from flask_restful import Api
from flask_script import Manager

from discounts_finder.api.url_processing import ProductsUrlProcessing
from discounts_finder.celery_init import make_celery
from discounts_finder.mongo import mongo

app = Flask(__name__)
app.config.from_object("config.Config")

api = Api(app)
mongo.init_app(app)

manager = Manager(app)
celery = make_celery()

api.add_resource(ProductsUrlProcessing, "/api/products_url")

if __name__ == "__main__":
    manager.run()
