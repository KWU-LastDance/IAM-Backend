import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float
from sqlalchemy.orm import relationship

from app.db.base import Base


class QualityClassification(Base):
    __tablename__ = 'quality_classification'

    id = Column(Integer, primary_key=True)
    image_id = Column(String)
    classification_result = Column(String)
    weight = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    products_id = Column(Integer, ForeignKey('products.id'))

    products = relationship('Products', back_populates='quality_classification')
