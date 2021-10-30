import logging
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
    results: Optional[List[WebShopProduct]]
    timestamp: float
    count: int


@dataclass
class ProductsTaskRead(ProductsTaskCreate):
    _id: str


@dataclass
class ProductsTaskUpdate(ProductsTaskRead):
    page_url: Optional[str] = None
    status: Optional[str] = None
    results: Optional[List[WebShopProduct]] = None
    timestamp: Optional[float] = None
    count: Optional[int] = None
    _id: Optional[str] = None


class ProductsTaskRepository:
    COLLECTION_NAME = "discounts_finder_tasks"

    def __init__(self):
        self._mongo_collection = MongoCollection(self.COLLECTION_NAME)

    def add_products_task(self, products_task: ProductsTaskCreate):
        return self._mongo_collection.add_object(asdict(products_task))

    def set_products_result(self, object_id: str, products: List[WebShopProduct]):
        updated = ProductsTaskUpdate(results=products, count=len(products), status=ProductsTaskUpdate.STATUS_COMPLETED)
        update_query = {k: v for k, v in asdict(updated).items() if v is not None}
        return self._mongo_collection.update_by_id(
            object_id,
            update_query
        )

    def get_products_result(self, object_id) -> ProductsTaskRead:
        products_task = self._mongo_collection.get_by_id(object_id)
        products_task["_id"] = str(products_task["_id"])
        return ProductsTaskRead(**products_task)
