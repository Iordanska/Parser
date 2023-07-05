from json import dumps
from typing import List

from kafka import KafkaProducer

from category.schema import Category
from config.base_settings import settings
from product.schema import Product


def get_producer():
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda x: dumps(x, default=str).encode("utf-8"),
    )
    return producer


def produce_categories(producer: KafkaProducer, data: List[Category]):
    for category in data:
        category = category.__dict__
        producer.send(settings.KAFKA_CATEGORIES_TOPIC, value=category)


def produce(producer: KafkaProducer, data: List[Product]):
    for product in data:
        product = product.__dict__
        producer.send(settings.KAFKA_PRODUCTS_TOPIC, value=product)
