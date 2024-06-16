from typing import Optional
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    stock: Optional[int] = None


class ProductUpdate(ProductBase):
    pass


class ProductCreate(ProductBase):
    name: str
    description: str
    category: str


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
