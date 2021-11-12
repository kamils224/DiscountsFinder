from dataclasses import asdict

from flask_restful import Resource
from flask_restful import reqparse

from discounts_finder.services.discount_finder_service import DiscountsFinderService


class DiscountFinderJob(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument("url", type=str)
        args = parser.parse_args()
        url = args["url"]

        task_service = DiscountsFinderService()
        result = task_service.process_single_url(url)

        return {"object_id": result.id, "status": result.status}

    @staticmethod
    def get(object_id: str):
        task_service = DiscountsFinderService()
        result = task_service.get_single_url_result(object_id)
        print("result get")
        print(result)
        return asdict(result)
