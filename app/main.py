from fastapi import FastAPI

from app.api.v1.endpoints import products_controller

app = FastAPI()

app.include_router(products_controller.router, prefix="/products", tags=["products"])
