from pydantic import BaseModel
from typing import List

class ProductItemInput(BaseModel):
    product_id: str
    name: str
    quantity: int
    price: float
    
class SaleCreate(BaseModel):
    products: List[ProductItemInput]
    total: float
    
class SaleOut(SaleCreate):
    id: str
    user_id: str