from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from src.infrastructure.security import get_current_user
from src.adapters.api.schemas.product_schema import ProductCreate, ProductOut
from src.core.entities.product import Product
from src.adapters.db.mongo_repository import (create_product, 
    list_products, get_product_by_id, update_product, delete_product,
    add_image_to_product,
    remove_image_from_product)
from typing import Dict
import cloudinary.uploader
from uuid import uuid4

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

@router.post("/upload-image/{product_id}", status_code=201)
async def upload_image(
    product_id: str,
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    try:
        result = cloudinary.uploader.upload(
            file.file,
            folder="products",
            public_id=str(uuid4()),
            resource_type="image"
        )
        
        image_data = {
            "url": result["secure_url"],
            "public_id": result["public_id"]
        }
        
        updated = add_image_to_product(product_id, image_data)
        
        if not updated:
            raise HTTPException(status_code=404, detail="Produto não encontrado para adicionar imagem")
        
        return image_data
    except Exception as e:
        raise HTTPException(status=500, detail=f"Erro ao fazer upload: {e}")
    
@router.delete("/delete-image/{product_id}/{public_id}")
async def delete_image(product_id: str, public_id: str, user=Depends(get_current_user)):
        try:
            result = cloudinary.uploader.destroy(public_id)
            
            if result.get("result") != "ok":
                raise HTTPException(status_code=400, detail="Erro ao excluir no Cloudnary")
            
            success = remove_image_from_product(product_id, public_id)
            
            if not success:
                raise HTTPException(status_code=404, detail="Imagem não encontrada no produto")
            
            return {"detail": "Imagem excluída com sucesso"}
        except Exception as e:
            raise HTTPException(status=500, detail=f"Erro ao excluir imagem {e}")