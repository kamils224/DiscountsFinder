from dataclasses import asdict

from discounts_finder.mongo import MongoCollection
from discounts_finder.parsers.products_finder.models import WebShopProduct


class ProductsService:
    COLLECTION_NAME = "products_finder_tasks"

    def add_products(self, product: WebShopProduct):
        mongo_collection = MongoCollection(self.COLLECTION_NAME)
        return mongo_collection.add_object(asdict(product))
