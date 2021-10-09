from flask_restful import Resource
from flask_restful import reqparse

from discounts_finder.celery_worker.tasks import process_products_url


class DiscountFinderJob(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("url", type=str)
        args = parser.parse_args()
        url = args["url"]
        result = process_products_url.delay(url)

        return {"task_id": result.id, "status": "processing"}
