from datetime import datetime

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.endpoints.apple_classification_controller import apple_classification_service
from app.db.session import get_db
from app.repositories.transactions_repository import TransactionsRepository
from app.schemas.transactions import TransactionsDetailWithProduct, Transactions, TransactionsCreate, \
    InventoryHistoryResponse
from app.services.transactions_service import TransactionsService

router = APIRouter()

transactions_repository = TransactionsRepository()
transactions_service = TransactionsService(transactions_repository)
apple_classification_service.transactions_repository = transactions_repository


@router.get("/", response_model=list[Transactions])
def get_transactions(start: datetime = Query(None), end: datetime = Query(None), db: Session = Depends(get_db)):
    return transactions_service.get_transactions(start, end, db)


@router.get("/{transaction_id}", response_model=list[TransactionsDetailWithProduct])
def get_transaction_details(transaction_id: int, db: Session = Depends(get_db)):
    return transactions_service.get_transaction_details(transaction_id, db)


@router.post("/store")
def store_transaction(transaction: list[TransactionsCreate], db: Session = Depends(get_db)):
    try:
        new_transaction = transactions_service.store_transaction(transaction, db)
        return 'success'
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/release")
def release_transaction(transaction: list[TransactionsCreate], db: Session = Depends(get_db)):
    try:
        new_transaction = transactions_service.release_transaction(transaction, db)
        return 'success'
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{product_id}", response_model=list[InventoryHistoryResponse])
def get_inventory_history(
    product_id: int,
    db: Session = Depends(get_db),
    type: str = Query(None),
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    automated: bool = Query(None)
):
    return transactions_service.get_inventory_history(product_id, type, start_date, end_date, automated, db)