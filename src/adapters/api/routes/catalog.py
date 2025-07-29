from fastapi import APIRouter, Query
from src.adapters.api.schemas.product_schema import ProductOut
from src.adapters.db.mongo_repository import list_catalog_products

router = APIRouter(prefix="/catalog", tags=["Catálogo Digital Público"])

@router.get("/", response_model=list[ProductOut])
def catalog(
    name: str | None = Query(None, description="Buscar Nome"),
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
):
    products = list_catalog_products(name=name, min_price=min_price, max_price=max_price)
    return [ProductOut(**p.dict()) for p in products]