from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.transactions_repository import TransactionsRepository
from app.schemas.transactions import TransactionsCreate, InventoryHistoryResponse


class TransactionsService:
    def __init__(self, transactions_repository: TransactionsRepository):
        self.transactions_repository = transactions_repository

    def get_transactions(self, start: datetime, end: datetime, db: Session):
        transactions = self.transactions_repository.get_transactions_by_period(start, end, db)
        transactions.sort(key=lambda x: x.timestamp, reverse=True)
        return transactions

    def get_transaction_details(self, transaction_id: int, db: Session):
        data = self.transactions_repository.get_transaction_details(transaction_id, db)
        if not data:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return data

    def store_transaction(self, transaction: list[TransactionsCreate], db: Session):
        return self.transactions_repository.create(transaction, 'store', db)

    def release_transaction(self, transaction: list[TransactionsCreate], db: Session):
        return self.transactions_repository.create(transaction, 'release', db)

    def get_inventory_history(self,
                              product_id: int,
                              type: str,
                              start_date: datetime,
                              end_date: datetime,
                              automated: bool,
                              db: Session):
        history = self.transactions_repository.get_inventory_history(product_id, type, start_date, end_date, automated,
                                                                     db)
        result = []
        for transaction, detail, product in history:
            result.append(InventoryHistoryResponse(
                product_name=product.name,
                type=transaction.type,
                previous_stock=detail.previous_stock,
                current_stock=detail.current_stock,
                timestamp=transaction.timestamp,
                automated=transaction.automated
            ))
        return result
