import logging
from dataclasses import dataclass
from datetime import datetime

from discounts_finder.celery_worker.tasks import process_products_url
from discounts_finder.repositories.products_repository import ProductsTaskRepository, ProductsTask


@dataclass
class TaskResult:
    id: str
    status: str


class DiscountsFinderService:

    def __init__(self):
        self._tasks_repository = ProductsTaskRepository()

    def process_single_url(self, url: str) -> TaskResult:
        task = ProductsTask(
            page_url=url,
            status=ProductsTask.STATUS_PROCESSING,
            timestamp=datetime.timestamp(datetime.now()),
            products=None
        )
        result = self._tasks_repository.add_task(task)
        logging.info(result)
        task_result = TaskResult(str(result.inserted_id), ProductsTask.STATUS_PROCESSING)
        process_products_url.delay(task_result.id, url)

        return task_result
