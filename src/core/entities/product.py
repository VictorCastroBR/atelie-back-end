from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from src.adapters.api.schemas.product_schema import ProductImage

class Product(BaseModel):
    id: str | None = None
    name: str 
    description: str
    price: float
    stock: int
    images: Optional[List[ProductImage]] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
