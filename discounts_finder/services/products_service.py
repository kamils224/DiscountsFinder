from dataclasses import asdict

from discounts_finder.mongo import MongoConnector
from discounts_finder.parsers.products_finder.models import WebShopProduct


class ProductsService:
    TEMPORARY_PRODUCTS_COLLECTION_NAME = "temp_products"

    def add_products(self, product: WebShopProduct):
        mongo_db = MongoConnector(self.TEMPORARY_PRODUCTS_COLLECTION_NAME)
        return mongo_db.add_object(asdict(product))
