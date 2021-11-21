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

        result = DiscountsFinderService().process_single_url(url)

        return asdict(result)

    @staticmethod
    def get(object_id: str):
        result = DiscountsFinderService().get_single_url_result(object_id)
        return asdict(result)

    @staticmethod
    def delete(object_id: str):
        deleted = DiscountsFinderService().delete_single_url_result(object_id)
        status_code = 204 if deleted else 404
        return {"deleted": deleted}, status_code


class DiscountsFinderTasksList(Resource):
    @staticmethod
    def get():
        result = DiscountsFinderService().get_single_url_tasks()
        return [asdict(item) for item in result]
