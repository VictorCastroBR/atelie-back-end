from fastapi import FastAPI
from src.adapters.api.routes import auth, product, catalog, sales

app = FastAPI(title="Catálogo Digital")

app.include_router(auth.router)
app.include_router(product.router)
app.include_router(catalog.router)
app.include_router(sales.router)