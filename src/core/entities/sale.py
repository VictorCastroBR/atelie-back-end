from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class ProductItem(BaseModel):
    product_id: str
    name: str
    quantity: int
    price: float
    
class Sale(BaseModel):
    id: str | None = None
    user_id: str
    products: List[ProductItem]
    total: float
    created_at: datetime = datetime.utcnow()