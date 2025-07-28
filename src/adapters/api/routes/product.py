from fastapi import APIRouter, Depends, HTTPException
from src.infrastructure.security import get_current_user
from src.adapters.api.schemas.product_schema import ProductCreate, ProductOut
from src.core.entities.product import Product
from src.adapters.db.mongo_repository import create_product, list_products, get_product_by_id, update_product, delete_product

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

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: str):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return ProductOut(**product.dict())

@router.put("/{product_id}", response_model=ProductOut)
def update(product_id: str, data: ProductCreate, user=Depends(get_current_user)):
    updated = update_product(product_id, data.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Produto não encontrado para atualizar")
    return ProductOut(id=product_id, **data.dict())

@router.delete("/product")
def delete(product_id: str, user=Depends(get_current_user)):
    deleted = delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Produto não encontrado para deleter")
    return {"detail": "Produto deletado com sucesso"}