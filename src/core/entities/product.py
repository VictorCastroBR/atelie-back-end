from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class Product(BaseModel):
    id: str | None = None
    name: str 
    description: str
    price: float
    stock: int
    images: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
