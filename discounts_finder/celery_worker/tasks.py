import logging

from discounts_finder.celery_worker.celery_init import celery
from discounts_finder.parsers.network_utils import get_products_from_url
from discounts_finder.services.products_service import ProductsService


@celery.task()
def process_products_url(url):
    products = get_products_from_url(url)
    service = ProductsService()
    service.add_products(products[0])
    logging.info(products)
    return url
