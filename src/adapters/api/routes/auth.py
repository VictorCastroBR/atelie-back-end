from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from src.adapters.api.schemas.user_schema import UserCreate, UserLogin, UserOut
from src.core.entities.user import User
from src.adapters.db.mongo_repository import create_user, find_user_by_email, save_refresh_token, is_valid_refresh_token, invalidate_refresh_token
from src.infrastructure.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from jose import JWTError

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

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    save_refresh_token(refresh_token, user.email)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": user.role
    }
    
@router.post("/refresh")
def refresh_token(refresh_token: str = Body(...)):
    try:
        email = is_valid_refresh_token(refresh_token)
        if not email:
            raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado")

        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh" or payload.get("sub") != email:
            raise HTTPException(status_code=401, detail="Token inválido")

        invalidate_refresh_token(refresh_token)

        new_access = create_access_token({"sub": email})
        new_refresh = create_refresh_token({"sub": email})
        save_refresh_token(new_refresh, email)

        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")