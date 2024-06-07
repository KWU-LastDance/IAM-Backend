from sqlalchemy.orm import Session
from app.models.products import Products
from app.schemas.products import ProductCreate, ProductUpdate


class ProductsRepository:
    def create(self, product: ProductCreate, db: Session):
        product_data = product.dict(exclude_unset=True)
        db_product = Products(**product_data)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    def get_all(self, db: Session):
        return db.query(Products).filter(Products.deleted == False).all()

    def get_by_id(self, product_id: int, db: Session):
        return db.query(Products).filter(Products.id == product_id).first()

    def update(self, product_id: int, product: ProductUpdate, db: Session):
        product_data = {key: value for key, value in product.dict(exclude_unset=True).items()
                        if value is not None and value != ""}
        db.query(Products).filter(Products.id == product_id).update(product_data)
        db.commit()
        return db.query(Products).filter(Products.id == product_id).first()

    def delete(self, product_id: int, db: Session):
        product = db.query(Products).filter(Products.id == product_id).first()
        if product:
            product.deleted = True
            from datetime import datetime
            product.deleted_at = datetime.now()
            db.commit()
