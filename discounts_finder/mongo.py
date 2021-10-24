from pymongo import MongoClient
from typing import Any, Dict
import bson

from discounts_finder.config import Config

MONGO_DATABASE = "discounts_finder"


def get_mongo_db():
    """
    Configuration method to return mongo db instance
    """
    client = MongoClient(Config.MONGO_URI)
    return client[MONGO_DATABASE]


mongo_db = get_mongo_db()


class MongoCollection:

    def __init__(self, collection_name: str):
        self._collection_name = collection_name

    def add_object(self, obj: Dict[str, Any]):
        return mongo_db[self._collection_name].insert_one(obj)

    def update_by_id(self, obj_id: str, obj_to_update: Dict[str, Any]):
        return mongo_db[self._collection_name].update({"_id": bson.ObjectId(obj_id)}, {"$set": obj_to_update})
