from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str
    categories: List[str]
    brand: str
    brand_id: int
    sku: str
    price: float = Field(gt=0)
    old_price: float | None
    discount: int | None = Field(gt=0, lt=101)
    color: str | None
    image_links: List[str] | None
    url: str
    rating: float | None
    reviews: int | None
    created_at: datetime
