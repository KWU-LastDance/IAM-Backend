from fastapi import FastAPI

from app.api.v1.endpoints import products_controller
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
