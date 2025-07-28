from fastapi import FastAPI
from src.adapters.api.routes import auth

app = FastAPI(title="Catálogo Digital")

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Catálogo Digital API funcionando"}
