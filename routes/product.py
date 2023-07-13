from fastapi import APIRouter, Depends

from DAOs.product import ProductDAO, get_product_dao
from schemas.product import Product

router = APIRouter()


@router.get("/", response_description="List all products")
async def list_products(dao: ProductDAO = Depends(get_product_dao)):
    products = dao.get_products()
    return {"products": products}


@router.post("/", response_description="Add product")
async def add_product(product: Product, dao: ProductDAO = Depends(get_product_dao)):
    id = dao.create_product(product)
    return {"product_id": id}
