import datetime

from sqlalchemy import Column, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    quantity = Column(Integer)
    automated = Column(Boolean)
    memo = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    transactions_detail = relationship('TransactionsDetail', back_populates='transaction')