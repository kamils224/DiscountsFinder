import logging

from discounts_finder.celery_worker.celery_init import celery
from discounts_finder.parsers.network_utils import get_products_from_url
from discounts_finder.repositories.products_tasks_repository import (
    ProductsTaskRepository,
    ProductsTaskRead,
)


@celery.task()
def process_products_url(object_id: str, url: str) -> None:
    products = get_products_from_url(url)
    products_tasks_repository = ProductsTaskRepository()

    logging.info(f"Updating task result for {object_id}")
    products_tasks_repository.update(
        object_id,
        {
            "results": products,
            "count": len(products),
            "status": ProductsTaskRead.STATUS_COMPLETED,
        },
    )

    logging.info("Task completed")
