from datetime import datetime

import pytz
from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    quantity = Column(Integer)
    variation = Column(Integer)
    automated = Column(Boolean, default=False)
    memo = Column(String)
    timestamp = Column(DateTime, default=datetime.now(tz=pytz.timezone('Asia/Seoul')).replace(microsecond=0))

    transactions_detail = relationship('TransactionsDetail', back_populates='transactions')


class TransactionsDetail(Base):
    __tablename__ = 'transactions_detail'

    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    previous_stock = Column(Integer)
    current_stock = Column(Integer)

    transactions = relationship('Transactions', back_populates='transactions_detail')
    products = relationship('Products', back_populates='transactions_detail', uselist=False)
