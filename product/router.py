from fastapi import APIRouter, Depends

from product.dao import ProductDAO, get_product_dao
from product.schema import Product

product_router = APIRouter()


@product_router.get("/", response_description="List all products")
async def list_products(dao: ProductDAO = Depends(get_product_dao)):
    products = dao.get_products()
    return {"products": products}


@product_router.post("/", response_description="Add product")
async def add_product(product: Product, dao: ProductDAO = Depends(get_product_dao)):
    id = dao.create_product(product)
    return {"product_id": id}
