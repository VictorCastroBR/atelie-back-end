from fastapi import APIRouter, HTTPException, Depends
from src.infrastructure.security import get_current_user
from src.adapters.api.schemas.store_schema import StoreOut, StoreCreate
from src.core.entities.store import Store
from src.adapters.db.mongo_repository import get_store, isThereAStore, register_store

router = APIRouter(prefix="/store", tags=["Configurações da Loja"])

@router.get("/", response_model=StoreOut)
def index(user=Depends(get_current_user)):
    store = get_store()
    if not store:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    return StoreOut(**store.dict())

@router.post("/", response_model=StoreOut)
def create_store(data: StoreCreate, user=Depends(get_current_user)):
    store = Store(**data.dict())
    if isThereAStore():
        raise HTTPException(status_code=409, detail="A loja já foi cadastrada, se necessário, atualize-a")
    store_id = register_store(store)
    return StoreOut(id=store_id, **store.dict())