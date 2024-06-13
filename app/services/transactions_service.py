from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.transactions_repository import TransactionsRepository
from app.schemas.transactions import TransactionsCreate


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
