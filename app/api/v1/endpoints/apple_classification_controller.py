from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.apple_classification_repository import AppleClassificationRepository
from app.schemas.apple_classification import AppleClassificationRottenResponse, AppleClassificationWeightResponse, \
    AppleClassificationQualityResponse, StockStatusResponse
from app.services.apple_classfication_service import AppleClassificationService

router = APIRouter()

apple_classification_repository = AppleClassificationRepository()
apple_classification_service = AppleClassificationService(apple_classification_repository)


@router.get("/coding-apple", response_model=AppleClassificationRottenResponse)
async def get_apple_status(db: Session = Depends(get_db)):
    apple_code = apple_classification_service.make_new_apple(db)
    return apple_classification_service.get_apple_rotten(apple_code, db)


@router.get("/weight-apple/{apple_code}", response_model=AppleClassificationWeightResponse)
async def get_apple_weight(apple_code: str, db: Session = Depends(get_db)):
    return apple_classification_service.get_apple_weight(apple_code, db)


@router.get("/nice-apple/{apple_code}", response_model=AppleClassificationQualityResponse)
async def get_apple_quality(apple_code: str, db: Session = Depends(get_db)):
    return apple_classification_service.get_apple_quality(apple_code, db)


@router.get("/current", response_model=StockStatusResponse)
async def get_stock_status():
    return apple_classification_service.get_stock_status()
