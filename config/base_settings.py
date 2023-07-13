import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_LINK: str
    MONGO_USER: str
    MONGO_PASSWORD: str
    DB_NAME: str
    DB_PRODUCT_COLLECTION: str
    DB_CATEGORY_COLLECTION: str
    KAFKA_HOST: str
    KAFKA_PORT: str
    KAFKA_TOPIC: str

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__file__))}/../.env"
        env_file_encoding = "utf-8"


settings = Settings(
    _env_file=f"{os.path.dirname(os.path.abspath(__file__))}/../.env",
    _env_file_encoding="utf-8",
)
