from celery import shared_task


@shared_task
def test():
    return 5 + 10
