from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.adapters.api.routes import auth, product, catalog, sales

app = FastAPI(title="Catálogo Digital")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(product.router)
app.include_router(catalog.router)
app.include_router(sales.router)