import hashlib
import uuid

from sqlalchemy.orm import Session

import random

from app.schemas.apple_classification import StockStatusResponse, AppleClassificationCreate, \
    AppleClassificationRottenResponse, AppleClassificationQualityResponse, AppleClassificationWeightResponse


class AppleClassificationService:
    def __init__(self, apple_classification_repository):
        self.apple_classification_repository = apple_classification_repository
        self.stock_special = 0
        self.stock_good = 0
        self.stock_bad = 0
        self.stock_rotten = 0

    def check_stock(self):
        if self.stock_special >= 20:
            self.stock_special -= 20
            # TODO: 사과 - 특상 입고 처리
        if self.stock_good >= 20:
            self.stock_good -= 20
            # TODO: 사과 - 상 입고 처리
        if self.stock_bad >= 20:
            self.stock_bad -= 20
            # TODO: 사과 - 하 입고 처리

    def create_apple_metadata(self):
        hashed_uuid = hashlib.sha256(uuid.uuid4().bytes).hexdigest()[:16]
        weight = max(269, min(int(random.gauss(319, 5)), 379))
        rotten = random.choices([True, False], weights=[4, 96], k=1)[0]
        if not rotten:
            image_class = random.choices(["special", "good", "bad"], weights=[25, 45, 30], k=1)[0]
        else:
            image_class = None
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
        if raw_data.image_class == "special":
            self.stock_special += 1
        elif raw_data.image_class == "good":
            self.stock_good += 1
        elif raw_data.image_class == "bad":
            self.stock_bad += 1
        return self.apple_classification_repository.create(raw_data, db).apple_code

    def get_apple_rotten(self, apple_code: str, db: Session):
        date = self.apple_classification_repository.get_status_by_apple_code(apple_code, db)
        return AppleClassificationRottenResponse(apple_code=apple_code, rotten=date.rotten)

    def get_apple_weight(self, apple_code: str, db: Session):
        data = self.apple_classification_repository.get_status_by_apple_code(apple_code, db)
        return AppleClassificationWeightResponse(apple_code=apple_code, rotten=data.rotten, weight=data.weight)

    def get_apple_quality(self, apple_code: str, db: Session):
        data = self.apple_classification_repository.get_status_by_apple_code(apple_code, db)
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
