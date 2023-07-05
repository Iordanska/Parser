from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from config.base_settings import settings


def get_database() -> Database:
    client = MongoClient(settings.MONGO_LINK)
    db = client[settings.DB_NAME]
    return db


def get_product_collection() -> Collection:
    collection = get_database()[settings.DB_PRODUCT_COLLECTION]
    return collection


def get_category_collection() -> Collection:
    collection = get_database()[settings.DB_CATEGORY_COLLECTION]
    return collection
