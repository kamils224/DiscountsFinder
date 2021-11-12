from dataclasses import asdict, dataclass
from typing import Optional, List, Any, Union, Dict

from discounts_finder.mongo import MongoCollection
from discounts_finder.parsers.products_finder.models import WebShopProduct
from discounts_finder.repositories.base_repository import BaseRepository


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


class ProductsTaskRepository(BaseRepository):
    COLLECTION_NAME = "discounts_finder_tasks"

    def __init__(self):
        self._mongo_collection = MongoCollection(self.COLLECTION_NAME)

    def create(self, obj: ProductsTaskCreate) -> Union[str, int]:
        created = self._mongo_collection.add_object(asdict(obj))
        return str(created.inserted_id)

    def read(self, obj_id: Union[str, int]) -> ProductsTaskRead:
        products_task = self._mongo_collection.get_by_id(obj_id)
        _id = str(products_task.pop("_id"))
        return ProductsTaskRead(_id=_id, **products_task)

    def update(self, obj_id: Union[str, int], fields: Dict[str, Any], allow_none: bool = False):
        update_query = fields
        if not allow_none:
            update_query = {k: v for k, v in update_query if v is not None}
        return self._mongo_collection.update_by_id(
            obj_id,
            update_query
        )

    def delete(self, obj_id: Union[str, int]):
        raise NotImplementedError()

    def read_all(self):
        raise NotImplementedError()
