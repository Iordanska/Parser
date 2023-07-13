from fastapi import Depends
from pymongo.collection import Collection

from config.db import get_category_collection
from schemas.category import Category
from serializers.category import categories_serializer, category_serializer


class CategoryDAO:
    def __init__(self, collection: Collection):
        self.collection = get_category_collection()

    def get_categories(self):
        categories = categories_serializer(self.collection.find())
        return categories

    def get_category_by_id(self, id):
        category = self.collection.find_one({"category_id": id})
        if category:
            category = category_serializer(category)
        return category

    def create_category(self, category: Category):
        product = self.collection.insert_one(category)
        category_id = str(product.inserted_id)
        return category_id


def get_category_dao(collection: Collection = Depends(get_category_collection)):
    return CategoryDAO(collection)
