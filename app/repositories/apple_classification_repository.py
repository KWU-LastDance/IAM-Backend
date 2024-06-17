from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.apple_classification import AppleClassificationCreate
from app.models.apple_classification import AppleClassification


class AppleClassificationRepository:
    def create(self, raw_data: AppleClassificationCreate, db: Session):
        db_data = raw_data.dict(exclude_unset=True)
        db_data = AppleClassification(**db_data)
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
        return db_data

    def get_status_by_apple_code(self, apple_code: str, db: Session):
        data = db.query(AppleClassification).filter(AppleClassification.apple_code == apple_code).first()
        if data is None:
            raise HTTPException(status_code=404, detail="Apple not found")
        return data
