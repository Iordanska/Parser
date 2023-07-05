import threading
from parser import parse_category

from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from kafka import KafkaProducer

from category.dao import CategoryDAO, get_category_dao
from category.parser import parse_categories
from category.router import category_router
from config.db import get_category_collection, get_product_collection
from config.exception_handlers import request_validation_exception_handler
from consumer import (
    consume_categories,
    consume_products,
    get_category_consumer,
    get_product_consumer,
)
from producer import get_producer, produce, produce_categories
from product.dao import ProductDAO
from product.router import product_router

app = FastAPI(title="Lamoda parser")
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(category_router, prefix="/categories", tags=["categories"])
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)


@app.on_event("startup")
async def startup_event():
    product_collection = get_product_collection()
    product_dao = ProductDAO(product_collection)
    consumer_thread1 = threading.Thread(target=consume_products, args=(product_dao,))
    consumer_thread1.start()

    category_collection = get_category_collection()
    category_dao = CategoryDAO(category_collection)
    consumer_thread2 = threading.Thread(target=consume_categories, args=(category_dao,))
    consumer_thread2.start()


@app.get("/get_cats", response_description="Parse all categories", tags=["parser"])
async def get_categories(producer: KafkaProducer = Depends(get_producer)):
    try:
        data = parse_categories()
    except:
        raise HTTPException(status_code=500, detail="Parser error")

    try:
        produce_categories(producer, data)
    except:
        raise HTTPException(status_code=500, detail="Producer error")
    return {"success": 'categories have been parsed"'}


@app.post(
    "/parse", response_description="Parse products from the category", tags=["parser"]
)
async def parse_products(
    category_id: str,
    dao: CategoryDAO = Depends(get_category_dao),
    producer: KafkaProducer = Depends(get_producer),
):
    category = dao.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    try:
        data = parse_category(category["link"])
    except:
        raise HTTPException(status_code=500, detail="Parser error")

    try:
        produce(producer, data)
    except:
        raise HTTPException(status_code=500, detail="Producer error")

    return {"success": f"category {category['name']} has been parsed"}


@app.on_event("shutdown")
async def shutdown_event():
    product_consumer = get_product_consumer()
    product_consumer.commit()
    product_consumer.close()

    category_consumer = get_category_consumer()
    category_consumer.commit()
    category_consumer.close()
