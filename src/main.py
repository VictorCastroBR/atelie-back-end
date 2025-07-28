from fastapi import FastAPI
from src.adapters.api.routes import auth
from src.adapters.api.routes import product

app = FastAPI(title="Catálogo Digital")

app.include_router(auth.router)
app.include_router(product.router)