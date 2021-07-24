from dataclasses import asdict

from flask_restful import Resource
from flask_restful import reqparse

from discounts_finder.parsers.network_utils import get_products_from_url
from discounts_finder.parsers.products_finder.models import WebShopProductSerializer

parser = reqparse.RequestParser()

class ProductsUrlProcessing(Resource):

    def post(self):
        parser.add_argument("url", type=str)
        args = parser.parse_args()
        url = args["url"]
        products = get_products_from_url(url)
        serializer = WebShopProductSerializer()
        return {"products": [serializer.dump(product) for product in products]}
