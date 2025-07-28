from pydantic import BaseModel
from typing import List

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    images: List[str] = []
    
class ProductOut(BaseModel):
    id: str
    name: str
    description: str
    price: float
    stock: int
    images: List[str]