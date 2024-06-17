from datetime import datetime
from typing import Optional, List

import pytz
from pydantic import BaseModel


class TransactionsBase(BaseModel):
    type: str
    quantity: int
    variation: int
    automated: bool
    memo: Optional[str] = None


class TransactionsCreate(BaseModel):
    product_id: int
    variation: int
    # timestamp: Optional[datetime] = datetime.now(tz=pytz.timezone('Asia/Seoul')).replace(microsecond=0)


class Transactions(TransactionsBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class TransactionsDetailBase(BaseModel):
    previous_stock: int
    current_stock: int


class TransactionsDetailCreate(TransactionsDetailBase):
    transaction_id: int
    variable: int
    timestamp: datetime


class TransactionsDetailWithProduct(TransactionsDetailBase):
    product_name: str


class InventoryHistoryResponse(BaseModel):
    product_name: str
    type: str
    previous_stock: int
    current_stock: int
    timestamp: datetime
    automated: bool
