import json
import logging

from kafka import KafkaConsumer

from category.dao import CategoryDAO
from config.base_settings import settings
from product.dao import ProductDAO

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.getLevelName(logging.DEBUG))


def get_product_consumer():
    consumer = KafkaConsumer(
        settings.KAFKA_PRODUCTS_TOPIC,
        group_id="products_group",
        auto_offset_reset="smallest",
        bootstrap_servers=["localhost:9092"],
        value_deserializer=lambda m: json.loads(m.decode("ascii")),
        enable_auto_commit=True,
    )
    return consumer


def get_category_consumer():
    consumer = KafkaConsumer(
        settings.KAFKA_CATEGORIES_TOPIC,
        group_id="category_group",
        auto_offset_reset="smallest",
        bootstrap_servers=["localhost:9092"],
        value_deserializer=lambda m: json.loads(m.decode("ascii")),
        enable_auto_commit=True,
    )
    return consumer


def consume_categories(dao: CategoryDAO):
    consumer = get_category_consumer()

    try:
        for msg in consumer:
            category = msg.value
            id = dao.create_category(category)
            logger.info("Category Data inserted with id " + str(id))
            consumer.commit()
    except KeyboardInterrupt:
        consumer.close()
    finally:
        consumer.close()


def consume_products(dao: ProductDAO):
    consumer = get_product_consumer()

    try:
        for msg in consumer:
            product = msg.value
            id = dao.create_product(product)
            logger.info("Data inserted with id " + str(id))
            consumer.commit()
    except KeyboardInterrupt:
        consumer.close()
    finally:
        consumer.close()
