from sqlalchemy.orm import Session

from app.models.products import Products
from app.models.transactions import Transactions, TransactionsDetail
from app.schemas.transactions import TransactionsCreate
from fastapi import HTTPException


class TransactionsRepository:
    def create(self, raw_data: list[TransactionsCreate], transactions_type: str, db: Session):
        try:
            with db.begin():
                transactions = Transactions(type=transactions_type, quantity=0, variation=0, automated=False, memo="")
                db.add(transactions)
                db.flush()  # ID를 얻기 위해 flush 호출
                for data in raw_data:
                    product = db.query(Products).filter(Products.id == data.product_id).first()
                    if not product:
                        raise HTTPException(status_code=404, detail=f"Product with id {data.product_id} not found")

                    transactions_detail = TransactionsDetail(
                        transaction_id=transactions.id,
                        product_id=data.product_id,
                        previous_stock=product.stock,
                        current_stock=0
                    )

                    if transactions_type == 'store':
                        transactions_detail.current_stock = transactions_detail.previous_stock + data.variation
                    elif transactions_type == 'release':
                        if transactions_detail.previous_stock < data.variation:
                            raise HTTPException(status_code=400, detail="재고가 부족하여 출고가 불가능합니다.")
                        transactions_detail.current_stock = transactions_detail.previous_stock - data.variation

                    product.stock = transactions_detail.current_stock  # 실제 제품 재고 업데이트
                    transactions.variation += data.variation
                    transactions.quantity += 1
                    db.add(transactions_detail)
                db.flush()  # 트랜잭션 내부에서 변경 사항을 반영
                db.refresh(transactions)  # 트랜잭션 내부에서 refresh 호출
            return transactions
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def auto_create(self, apple: TransactionsCreate, db: Session):
        try:
            with db.begin():
                transactions = Transactions(type='store', quantity=1, variation=apple.variation, automated=True,
                                            memo="IAM 시스템에 의해 자동으로 입고된 품목입니다.")
                db.add(transactions)
                db.flush()
                product = db.query(Products).filter(Products.id == apple.product_id).first()
                if not product:
                    raise HTTPException(status_code=404, detail=f"Product with id {apple.product_id} not found")

                transactions_detail = TransactionsDetail(
                    transaction_id=transactions.id,
                    product_id=apple.product_id,
                    previous_stock=product.stock,
                    current_stock=product.stock + apple.variation
                )

                product.stock = transactions_detail.current_stock
                transactions.variation += apple.variation
                db.add(transactions_detail)
                db.flush()
                db.refresh(transactions)
            return transactions
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def get_transactions_by_period(self, start, end, db):
        if start and end:
            return db.query(Transactions).filter(Transactions.timestamp >= start, Transactions.timestamp <= end).all()
        elif start:
            return db.query(Transactions).filter(Transactions.timestamp >= start).all()
        elif end:
            return db.query(Transactions).filter(Transactions.timestamp <= end).all()
        else:
            return db.query(Transactions).all()

    def get_transaction_details(self, transaction_id, db):
        transaction_details = db.query(
            Products.name.label('product_name'),
            TransactionsDetail.previous_stock,
            TransactionsDetail.current_stock,
        ).join(Products, TransactionsDetail.product_id == Products.id).filter(
            TransactionsDetail.transaction_id == transaction_id
        ).all()

        if not transaction_details:
            raise HTTPException(status_code=404, detail=f"No details found for transaction ID {transaction_id}")

        return transaction_details
