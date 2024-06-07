from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.products_repository import ProductsRepository
from app.schemas.products import Product, ProductCreate
from app.services.products_service import ProductsService

router = APIRouter()

products_repository = ProductsRepository()
products_service = ProductsService(products_repository)


@router.get("/", response_model=list[Product])
async def get_all_products(db: Session = Depends(get_db)):
    return products_service.get_all(db)


@router.post("/", response_model=Product)
async def create_product(product_create: ProductCreate, db: Session = Depends(get_db)):
    return products_service.create(product_create, db)


@router.get("/{product_id}", response_model=Product)
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return products_service.get_by_id(product_id, db)


@router.patch("/{product_id}", response_model=Product)
async def update_product(product_id: int, product_create: ProductCreate, db: Session = Depends(get_db)):
    return products_service.update(product_id, product_create, db)


@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    return products_service.delete(product_id, db)