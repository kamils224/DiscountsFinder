from dataclasses import asdict, dataclass
from typing import Optional, List, Any, Union, Dict

from discounts_finder.mongo import MongoCollection
from discounts_finder.parsers.products_finder.models import WebShopProduct
from discounts_finder.repositories.base_repository import BaseRepository, BaseDto


@dataclass
class ProductsTaskCreate(BaseDto):
    STATUS_COMPLETED = "COMPLETED"
    STATUS_PROCESSING = "PROCESSING"
    STATUS_FAILED = "FAILED"

    page_url: str
    status: str
    timestamp: float
    count: int
    results_timestamp: Optional[float] = None
    results: Optional[List[WebShopProduct]] = None

    @classmethod
    def from_dict(cls, dict_obj: Dict[str, Any]) -> ["ProductsTaskCreate"]:
        return cls(**dict_obj)


@dataclass
class ProductsTaskRead(ProductsTaskCreate):
    _id: str = None
    page_url: Optional[str] = None
    status: Optional[str] = None
    timestamp: Optional[float] = None
    count: Optional[int] = None
    results: Optional[List[WebShopProduct]] = None

    @classmethod
    def from_dict(cls, dict_obj: Dict[str, Any]) -> ["ProductsTaskRead"]:
        _id = str(dict_obj.pop("_id"))
        return cls(_id=_id, **dict_obj)


class ProductsTaskRepository(BaseRepository):
    COLLECTION_NAME = "discounts_finder_tasks"

    def __init__(self):
        self._mongo_collection = MongoCollection(self.COLLECTION_NAME)

    def create(self, obj: ProductsTaskCreate) -> Union[str, int]:
        created = self._mongo_collection.add_object(asdict(obj))
        return str(created.inserted_id)

    def read(self, obj_id: Union[str, int]) -> ProductsTaskRead:
        products_task = self._mongo_collection.get_by_id(obj_id)
        return ProductsTaskRead.from_dict(products_task)

    def update(
        self, obj_id: Union[str, int], fields: Dict[str, Any], allow_none: bool = False
    ) -> Union[str, int]:
        update_query = fields
        if not allow_none:
            update_query = {k: v for k, v in update_query.items() if v is not None}
        updated = self._mongo_collection.update_by_id(obj_id, update_query)
        return updated.upserted_id

    def delete(self, obj_id: Union[str, int]):
        raise NotImplementedError()

    def read_all(self, exclude_fields: List[str] = None) -> List[ProductsTaskRead]:
        products_tasks = self._mongo_collection.all(exclude=exclude_fields)
        return [
            ProductsTaskRead.from_dict(product_task) for product_task in products_tasks
        ]
