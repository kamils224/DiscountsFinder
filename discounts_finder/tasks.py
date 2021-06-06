from celery_init import celery


@celery.task()
def process_products_url(url):
    return url
