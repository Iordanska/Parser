from fastapi import Depends
from pymongo.collection import Collection

from config.db import get_product_collection
from product.model import products_serializer
from product.schema import Product


class ProductDAO:
    def __init__(self, collection: Collection):
        self.collection = collection

    def get_products(self):
        products = products_serializer(self.collection.find())
        return products

    def create_product(self, product: Product):
        if type(product) is not dict:
            product = product.dict()
        product = self.collection.insert_one(product)
        product_id = str(product.inserted_id)
        return product_id


def get_product_dao(collection: Collection = Depends(get_product_collection)):
    return ProductDAO(collection)
