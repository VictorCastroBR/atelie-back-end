from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    street: str
    number: int
    district: str
    city: str
    state: str
    
class StoreImage(BaseModel):
    url: str = None
    public_url: str = None

class Store(BaseModel):
    id: str
    name: str
    cnpj: str
    phone_number: str
    is_open: bool
    img: Optional[StoreImage]
    address: Optional[Address]
    
class StoreOut(BaseModel):
    id: str
    name: str
    cnpj: str
    phone_number: str
    is_open: bool
    img: Optional[StoreImage]
    address: Optional[Address]
    
class StoreCreate(BaseModel):
    name: str
    cnpj: str
    phone_number: str
    is_open: bool = True
    img: Optional[StoreImage] = None
    address: Optional[Address] = None