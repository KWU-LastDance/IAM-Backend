from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class TransactionsDetail(Base):
    __tablename__ = 'transactions_detail'

    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    previous_stock = Column(Integer)
    current_stock = Column(Integer)

    transaction = relationship('Transaction', back_populates='transactions_detail')
    product = relationship('Products', back_populates='transactions_detail', uselist=False)
