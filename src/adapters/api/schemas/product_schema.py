from pydantic import BaseModel
from typing import Optional, List

class ProductImage(BaseModel):
    url: str
    public_id: str

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    images: Optional[List[ProductImage]] = []
    
class ProductOut(BaseModel):
    id: str
    name: str
    description: str
    price: float
    stock: int
    images: Optional[List[ProductImage]] = []