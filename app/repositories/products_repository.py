from sqlalchemy.orm import Session
from app.models.products import Products
from app.schemas.products import ProductCreate


class ProductsRepository:
    def create(self, product: ProductCreate, db: Session):
        product_data = product.dict(exclude_unset=True)
        db_product = Products(**product_data)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    def get_all(self, db: Session):
        return db.query(Products).all()

    def get_by_id(self, product_id: int, db: Session):
        return db.query(Products).filter(Products.id == product_id).first()
    