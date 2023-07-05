from fastapi import APIRouter, Depends

from category.dao import CategoryDAO, get_category_dao

category_router = APIRouter()


@category_router.get("/", response_description="List all categories")
async def list_categories(dao: CategoryDAO = Depends(get_category_dao)):
    categories = dao.get_categories()
    return {"categories": categories}
