from pymongo import MongoClient
from typing import Any, Dict, Optional
from bson import ObjectId

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
        self._collection = mongo_db[self._collection_name]

    def add_object(self, obj: Dict[str, Any]):
        return self._collection.insert_one(obj)

    def update_by_id(self, object_id: str, obj_to_update: Dict[str, Any]):
        return self._collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": obj_to_update}
        )

    def get_by_id(self, object_id):
        return self._collection.find_one({"_id": ObjectId(object_id)})

    def get_collection(self):
        return self._collection
