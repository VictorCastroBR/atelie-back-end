from fastapi import APIRouter, HTTPException
from src.adapters.api.schemas.user_schema import UserCreate, UserLogin, UserOut
from src.core.entities.user import User
from src.adapters.db.mongo_repository import create_user, find_user_by_email
from src.infrastructure.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register", response_model=UserOut)
def register(data: UserCreate):
    if find_user_by_email(data.email):
        raise HTTPException(status_code=400, detail="E-mail já registrado")
    hashed = hash_password(data.password)
    user = User(email=data.email, hashed_password=hashed, role="admin")
    user_id  = create_user(user)
    return UserOut(id=user_id, email=user.email, role=user.role)

@router.post("/login")
def login(data: UserLogin):
    user = find_user_by_email(data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token({"sub": user.email})
    return {"acess_token": token, "token_type": "beaer"}
