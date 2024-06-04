from fastapi import FastAPI

from app.api.v1.endpoints import hello_controller

app = FastAPI()

app.include_router(hello_controller.router, prefix="/hello", tags=["hello"])

