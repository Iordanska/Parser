from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from kafka import KafkaProducer

from DAOs.category import CategoryDAO, get_category_dao
from func.lamoda_parser import parse_categories, parse_category
from func.twitch_parser import parse_streams
from producer import get_producer, produce

router = APIRouter()


@router.get("/get_streams", response_description="Parse streams", tags=["parser"])
async def get_streams(
    game_id: str | None = None,
    user_login: str | None = None,
    producer: KafkaProducer = Depends(get_producer),
):
    try:
        data = parse_streams(game_id, user_login)
    except HTTPException:
        raise HTTPException(status_code=400, detail="Bad Request")
    except:
        raise HTTPException(status_code=500, detail="Parser error")

    try:
        produce(producer, data)
    except:
        raise HTTPException(status_code=500, detail="Producer error")

    return {"success": "streams have been parsed"}


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
