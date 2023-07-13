import json
import logging

from kafka import KafkaConsumer

from config.base_settings import settings
from DAOs.category import CategoryDAO
from DAOs.product import ProductDAO

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.getLevelName(logging.DEBUG))


def get_consumer():
    consumer = KafkaConsumer(
        settings.KAFKA_TOPIC,
        group_id="products_group",
        auto_offset_reset="smallest",
        bootstrap_servers=[f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}"],
        value_deserializer=lambda m: json.loads(m.decode("ascii")),
        enable_auto_commit=True,
        api_version=(7, 3, 2),
    )
    return consumer


def consume(category_dao: CategoryDAO, product_dao: ProductDAO):
    consumer = get_consumer()
    try:
        for msg in consumer:
            if msg.value.get("category_id"):
                id = category_dao.create_category(msg.value)
                logger.info("Category Data inserted with id " + str(id))
            else:
                id = product_dao.create_product(msg.value)
                logger.info("Data inserted with id " + str(id))
            consumer.commit()
    except KeyboardInterrupt:
        consumer.close()
    finally:
        consumer.close()
