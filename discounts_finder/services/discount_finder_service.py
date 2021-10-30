from dataclasses import dataclass
from datetime import datetime

from discounts_finder.celery_worker.tasks import process_products_url
from discounts_finder.repositories.products_tasks_repository import ProductsTaskRepository, ProductsTaskCreate, \
    ProductsTaskRead


@dataclass
class TaskResult:
    id: str
    status: str


class DiscountsFinderService:

    def __init__(self):
        self._tasks_repository = ProductsTaskRepository()

    def process_single_url(self, url: str) -> TaskResult:
        task = ProductsTaskCreate(
            page_url=url,
            status=ProductsTaskCreate.STATUS_PROCESSING,
            timestamp=datetime.timestamp(datetime.now()),
            results=None,
            count=0
        )
        result = self._tasks_repository.add_products_task(task)
        task_result = TaskResult(str(result.inserted_id), task.status)
        process_products_url.delay(task_result.id, url)

        return task_result

    def get_single_url_result(self, object_id: str) -> ProductsTaskRead:
        return self._tasks_repository.get_products_result(object_id)
