import logging

from flask_restful import reqparse
from flask_restful import Resource

from discounts_finder.tasks import process_products_url
from discounts_finder.parsers.network_utils import get_products_from_url
from discounts_finder.parsers.products_finder.models import ProductSchema

parser = reqparse.RequestParser()


class ProductsUrlProcessing(Resource):
    def post(self):
        parser.add_argument("url", type=str)
        args = parser.parse_args()
        url = args["url"]
        task = process_products_url.delay(url)
        result = next(task.collect())[-1]
        logging.warning(result)
        # products = get_products_from_url(url)
        # schema = ProductSchema()
        # return {"products": [schema.dump(product) for product in products]}
        return {"products": result}
