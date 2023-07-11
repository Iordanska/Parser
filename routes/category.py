from fastapi import APIRouter, Depends

from DAOs.category import CategoryDAO, get_category_dao

router = APIRouter()


@router.get("/", response_description="List all categories")
async def list_categories(dao: CategoryDAO = Depends(get_category_dao)):
    categories = dao.get_categories()
    return {"categories": categories}
