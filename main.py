import threading

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from config.db import get_category_collection, get_product_collection
from config.exception_handlers import request_validation_exception_handler
from consumer import consume, get_consumer
from DAOs.category import CategoryDAO
from DAOs.product import ProductDAO
from routes import category, parser, product

app = FastAPI(title="Lamoda parser")
app.include_router(product.router, prefix="/products", tags=["products"])
app.include_router(category.router, prefix="/categories", tags=["categories"])
app.include_router(parser.router, tags=["parser"])
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)


@app.on_event("startup")
async def startup_event():
    product_collection = get_product_collection()
    product_dao = ProductDAO(product_collection)
    category_collection = get_category_collection()
    category_dao = CategoryDAO(category_collection)

    consumer_thread = threading.Thread(target=consume, args=(category_dao, product_dao))
    consumer_thread.start()


@app.on_event("shutdown")
async def shutdown_event():
    consumer = get_consumer()
    consumer.commit()
    consumer.close()
