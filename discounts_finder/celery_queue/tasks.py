from discounts_finder.celery_queue.celery_init import celery


@celery.task()
def process_products_url(url):
    return url
