from pydantic import BaseModel, Field
from typing import Optional

class Address(BaseModel):
    street: str
    number: int
    district: str
    city: str
    state: str
    
class StoreImage(BaseModel):
    url: str

class Store(BaseModel):
    id: Optional[str] = None
    name: str
    cnpj: str
    phone_number: str
    is_open: bool
    img: Optional[StoreImage] = None
    address: Optional[Address] = None