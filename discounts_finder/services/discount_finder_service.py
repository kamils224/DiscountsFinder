from dataclasses import dataclass
from datetime import datetime
from typing import List

from discounts_finder.celery_worker.tasks import process_products_url
from discounts_finder.repositories.products_tasks_repository import (
    ProductsTaskRepository,
    ProductsTaskCreate,
    ProductsTaskRead,
)


@dataclass
class TaskResult:
    id: str
    status: str


class DiscountsFinderService:
    def __init__(self):
        self._products_tasks_repo = ProductsTaskRepository()

    def process_single_url(self, url: str) -> TaskResult:
        task = ProductsTaskCreate(
            page_url=url,
            status=ProductsTaskCreate.STATUS_PROCESSING,
            timestamp=datetime.timestamp(datetime.now()),
            results=None,
            count=0,
        )
        result_id = self._products_tasks_repo.create(task)
        task_result = TaskResult(result_id, task.status)
        process_products_url.delay(task_result.id, url)

        return task_result

    def get_single_url_result(self, object_id: str) -> ProductsTaskRead:
        return self._products_tasks_repo.read(object_id)

    def get_single_url_tasks(self) -> List[ProductsTaskRead]:
        return self._products_tasks_repo.read_all(exclude_fields=["results"])
