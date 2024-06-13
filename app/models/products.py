from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime
import datetime
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.rotten_classification import RottenClassification
from app.models.quality_classification import QualityClassification


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category = Column(String)
    stock = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    deleted_at = Column(DateTime, default=None)
    deleted = Column(Boolean, default=False)


Products.rotten_classification = relationship('RottenClassification', back_populates='products', uselist=False)
Products.quality_classification = relationship('QualityClassification', back_populates='products', uselist=False)
