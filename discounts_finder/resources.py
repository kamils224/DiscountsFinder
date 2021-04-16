from flask_restful import Resource

from schema import ProductSchema
from models import Product

products_schema = ProductSchema(many=True)


class Products(Resource):
    def get(self):
        products = Product.query.all()
        print("json")
        for p in products:
            print(p.price)
        return products_schema.dump(products)