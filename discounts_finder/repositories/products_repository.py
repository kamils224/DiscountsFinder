from dataclasses import asdict, dataclass
from typing import Optional, List

from discounts_finder.mongo import MongoCollection
from discounts_finder.parsers.products_finder.models import WebShopProduct


@dataclass
class ProductsTaskCreate:
    STATUS_COMPLETED = "COMPLETED"
    STATUS_PROCESSING = "PROCESSING"
    STATUS_FAILED = "FAILED"

    page_url: str
    status: str
    products: Optional[List[WebShopProduct]]
    timestamp: float


class ProductsTask(ProductsTaskCreate):
    _id: Optional[str]


class ProductsTaskRepository:
    COLLECTION_NAME = "products_finder_tasks"

    def __init__(self):
        self._mongo_collection = MongoCollection(self.COLLECTION_NAME)

    def add_task(self, products_task: ProductsTaskCreate):
        return self._mongo_collection.add_object(asdict(products_task))

    def update_products_for_task(self, obj_id: str, products: List[WebShopProduct]):
        new_products = [asdict(product) for product in products]
        return self._mongo_collection.update_by_id(
            obj_id, {"products": new_products, "status": ProductsTask.STATUS_COMPLETED}
        )
