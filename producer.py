from json import dumps

from kafka import KafkaProducer

from config.base_settings import settings


def get_producer():
    producer = KafkaProducer(
        bootstrap_servers=[f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}"],
        value_serializer=lambda x: dumps(x, default=str).encode("utf-8"),
        api_version=(7, 3, 2),
    )
    return producer


def produce(producer: KafkaProducer, data):
    for item in data:
        item = item.__dict__
        producer.send(settings.KAFKA_TOPIC, value=item)
