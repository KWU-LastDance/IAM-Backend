import hashlib
import uuid

from sqlalchemy.orm import Session

import random

from app.models.apple_classification import QualityEnum
from app.schemas.apple_classification import StockStatusResponse, AppleClassificationCreate, \
    AppleClassificationRottenResponse, AppleClassificationQualityResponse, AppleClassificationWeightResponse
from app.schemas.transactions import TransactionsCreate


class AppleClassificationService:
    def __init__(self, apple_classification_repository):
        self.apple_classification_repository = apple_classification_repository
        self.transactions_repository = None
        self.stock_special = 0
        self.stock_good = 0
        self.stock_bad = 0
        self.stock_rotten = 0

    def check_stock(self, image_class, db: Session):
        if image_class == QualityEnum.special:
            self.stock_special += 1
        elif image_class == QualityEnum.good:
            self.stock_good += 1
        elif image_class == QualityEnum.bad:
            self.stock_bad += 1

        if self.stock_special >= 20:
            self.stock_special -= 20
            self.transactions_repository.auto_create(TransactionsCreate(product_id=1, variation=20), db)
        if self.stock_good >= 20:
            self.stock_good -= 20
            self.transactions_repository.auto_create(TransactionsCreate(product_id=2, variation=20), db)
        if self.stock_bad >= 20:
            self.stock_bad -= 20
            self.transactions_repository.auto_create(TransactionsCreate(product_id=3, variation=20), db)

    def create_apple_metadata(self):
        hashed_uuid = hashlib.sha256(uuid.uuid4().bytes).hexdigest()[:16]
        weight = max(269, min(int(random.gauss(319, 5)), 379))
        rotten = random.choices([True, False], weights=[4, 96], k=1)[0]
        if not rotten:
            image_class = random.choices(["special", "good", "bad"], weights=[25, 45, 30], k=1)[0]
        else:
            image_class = "none"
        quality = image_class
        return {
            "apple_code": hashed_uuid,
            "weight": weight,
            "rotten": rotten,
            "image_class": image_class,
            "quality": quality
        }

    def make_new_apple(self, db: Session):
        raw_data = AppleClassificationCreate(**self.create_apple_metadata())
        if raw_data.rotten:
            self.stock_rotten += 1
        return self.apple_classification_repository.create(raw_data, db).apple_code

    def get_apple_rotten(self, apple_code: str, db: Session):
        date = self.apple_classification_repository.get_status_by_apple_code(apple_code, db)
        return AppleClassificationRottenResponse(apple_code=apple_code, rotten=date.rotten)

    def get_apple_weight(self, apple_code: str, db: Session):
        data = self.apple_classification_repository.get_status_by_apple_code(apple_code, db)
        return AppleClassificationWeightResponse(apple_code=apple_code, rotten=data.rotten, weight=data.weight)

    def get_apple_quality(self, apple_code: str, db: Session):
        data = self.apple_classification_repository.get_status_by_apple_code(apple_code, db)
        self.check_stock(data.image_class, db)
        return AppleClassificationQualityResponse(
            apple_code=apple_code,
            rotten=data.rotten,
            weight=data.weight,
            image_class=data.image_class,
            quality=data.quality
        )

    def get_stock_status(self):
        return StockStatusResponse(
            special=self.stock_special,
            good=self.stock_good,
            bad=self.stock_bad,
            rotten=self.stock_rotten
        )
