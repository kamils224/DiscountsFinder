from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

from discounts_finder.celery_worker.tasks import process_products_url
from discounts_finder.repositories.products_tasks_repository import (
    ProductsTaskRepository,
    ProductsTaskCreate,
    ProductsTaskRead,
)


class DiscountsFinderService:
    def __init__(self):
        self._products_tasks_repo = ProductsTaskRepository()

    def process_single_url(self, url: str) -> ProductsTaskRead:
        created_task = ProductsTaskCreate(
            page_url=url,
            status=ProductsTaskCreate.STATUS_PROCESSING,
            timestamp=datetime.timestamp(datetime.now()),
            results_timestamp=None,
            results=None,
            count=0,
        )
        result_id = self._products_tasks_repo.create(created_task)
        process_products_url.delay(result_id, url)
        return ProductsTaskRead(_id=result_id, **asdict(created_task))

    def get_single_url_result(self, object_id: str) -> ProductsTaskRead:
        return self._products_tasks_repo.read(object_id)

    def get_single_url_tasks(self) -> List[ProductsTaskRead]:
        return self._products_tasks_repo.read_all(exclude_fields=["results"])
