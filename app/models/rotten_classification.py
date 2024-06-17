import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class RottenClassification(Base):
    __tablename__ = 'rotten_classification'

    id = Column(Integer, primary_key=True)
    image_id = Column(String)
    classification_result = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    products_id = Column(Integer, ForeignKey('products.id'))

    products = relationship('Products', back_populates='rotten_classification')
