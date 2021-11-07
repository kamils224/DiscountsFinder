from dataclasses import asdict, dataclass
from typing import Optional, List, Any, Dict

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

    @classmethod
    def from_dict(cls, dict_obj: Dict[str, Any]):
        return cls(**dict_obj)


@dataclass
class ProductsTaskRead(ProductsTaskCreate):
    _id: str

    @classmethod
    def from_dict(cls, dict_obj: Dict[str, Any]):
        _id = str(dict_obj.pop("_id"))
        return cls(_id=_id, **dict_obj)


@dataclass
class ProductsTaskUpdate(ProductsTaskRead):
    _id: Optional[str] = None
    page_url: Optional[str] = None
    status: Optional[str] = None
    results: Optional[List[WebShopProduct]] = None
    timestamp: Optional[float] = None
    count: Optional[int] = None


@dataclass
class ProductsTaskListItem:
    _id: str
    page_url: str
    status: str
    timestamp: float
    count: int

    @classmethod
    def from_dict(cls, dict_obj: Dict[str, Any]):
        _id = str(dict_obj.pop("_id"))
        return cls(_id=_id, **dict_obj)


def create_products_task_dto(mongo_result) -> ProductsTaskRead:
    _id = str(mongo_result.pop("_id"))
    return ProductsTaskRead(_id=_id, **mongo_result)


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
        _id = str(products_task.pop("_id"))
        return ProductsTaskRead(_id=_id, **products_task)

    def get_products_tasks(self):
        products_tasks = self._mongo_collection.all(exclude=["results"])
        return [ProductsTaskListItem.from_dict(product_task) for product_task in products_tasks]
