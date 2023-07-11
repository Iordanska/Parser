from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from kafka import KafkaProducer

from config.db import get_category_collection, get_product_collection
from consumer import consume
from DAOs.category import CategoryDAO, get_category_dao
from DAOs.product import ProductDAO
from func.lamoda_parser import parse_categories, parse_category
from producer import get_producer, produce

router = APIRouter()


@router.get(
    "/get_categories", response_description="Parse all categories", tags=["parser"]
)
async def get_categories(producer: KafkaProducer = Depends(get_producer)):
    try:
        data = parse_categories()
    except:
        raise HTTPException(status_code=500, detail="Parser error")

    try:
        produce(producer, data)
    except:
        raise HTTPException(status_code=500, detail="Producer error")

    return {"success": "categories have been parsed"}


@router.post(
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
