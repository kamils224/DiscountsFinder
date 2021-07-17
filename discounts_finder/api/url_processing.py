from dataclasses import asdict

from flask_restful import Resource
from flask_restful import reqparse

from discounts_finder.parsers.network_utils import get_products_from_url

parser = reqparse.RequestParser()


class ProductsUrlProcessing(Resource):

    def post(self):
        parser.add_argument("url", type=str)
        args = parser.parse_args()
        url = args["url"]
        products = get_products_from_url(url)
        return {"products": [asdict(product) for product in products]}
