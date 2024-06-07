from sqlalchemy.orm import Session

from app.repositories.products_repository import ProductsRepository
from app.schemas.products import ProductCreate, ProductUpdate


class ProductsService:
    def __init__(self, product_repository: ProductsRepository):
        self.product_repository = product_repository

    def get_all(self, db: Session):
        return self.product_repository.get_all(db)

    def get_by_id(self, product_id: int, db: Session):
        return self.product_repository.get_by_id(product_id, db)

    def create(self, product_create: ProductCreate, db: Session):
        return self.product_repository.create(product_create, db)

    def update(self, product_id: int, product_update: ProductUpdate, db: Session):
        return self.product_repository.update(product_id, product_update, db)

    def delete(self, product_id, db):
        self.product_repository.delete(product_id, db)
