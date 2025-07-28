from fastapi import APIRouter, Depends
from src.infrastructure.security import get_current_user
from src.adapters.api.schemas.product_schema import ProductCreate, ProductOut
from src.core.entities.product import Product
from src.adapters.db.mongo_repository import create_product, list_products

router = APIRouter(prefix="/products", tags=["Produtos"])

@router.post("/", response_model=ProductOut)
def add_product(data: ProductCreate, user=Depends(get_current_user)):
    product = Product(**data.dict())
    product_id = create_product(product)
    return ProductOut(id=product_id, **data.dict())

@router.get("/", response_model=list[ProductOut])
def get_products():
    products = list_products()
    return [ProductOut(**p.dict()) for p in products]