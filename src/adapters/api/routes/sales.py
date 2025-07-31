from fastapi import APIRouter, Depends
from src.adapters.api.schemas.sale_schema import SaleCreate, SaleOut
from src.core.entities.sale import Sale
from src.adapters.db.mongo_repository import create_sale, list_sales_by_user
from src.infrastructure.security import get_current_user
from src.adapters.db.mongo_repository import find_user_by_email

router = APIRouter(prefix="/sales", tags=["Vendas"])

@router.post("/", response_model=SaleOut)
def register_sale(data: SaleCreate, user_email: str = Depends(get_current_user)):
    user = find_user_by_email(user_email)
    sale = Sale(user_id=user.id, products=data.products, total=data.total)
    sale_id = create_sale(sale)
    return SaleOut(id=sale_id, user_id=user.id, **data.dict())

@router.get("/", response_model=list[SaleOut])
def get_my_sales(user_email: str = Depends(get_current_user)):
    user = find_user_by_email(user_email)
    sales = list_sales_by_user(user.id)
    return [SaleOut(
        id=s.id, 
        user_id=s.user_id,
        products=s.products,
        total=s.total
    ) for s in sales]