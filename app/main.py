from fastapi import FastAPI

from app.api.v1.endpoints import products_controller
from app.db.session import init_db

app = FastAPI()


@app.on_event("startup")
async def startup():
    init_db()


app.include_router(products_controller.router, prefix="/products", tags=["products"])
