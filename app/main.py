from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import products_controller, monitoring_controller, apple_classification_controller, \
    transactions_controller
from app.db.session import init_db

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    init_db()


app.include_router(products_controller.router, prefix="/products", tags=["products"])
app.include_router(monitoring_controller.router, prefix="/monitoring-data", tags=["monitoring-data"])
app.include_router(apple_classification_controller.router, prefix="/dt", tags=["dt"])
app.include_router(transactions_controller.router, prefix="/transactions", tags=["transactions"])