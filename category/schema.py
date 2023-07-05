from pydantic import BaseModel


class Category(BaseModel):
    category_id: str
    name: str
    link: str
