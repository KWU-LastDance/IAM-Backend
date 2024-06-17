import datetime

from pydantic import BaseModel


class AppleClassificationBase(BaseModel):
    apple_code: str
    weight: int
    rotten: bool
    image_class: str
    quality: str


class AppleClassificationCreate(AppleClassificationBase):
    pass


class AppleClassification(AppleClassificationBase):
    id: int
    timestamp: datetime.datetime

    class Config:
        from_attributes = True


class AppleClassificationRottenResponse(BaseModel):
    apple_code: str
    rotten: bool


class AppleClassificationWeightResponse(BaseModel):
    apple_code: str
    rotten: bool
    weight: int


class AppleClassificationQualityResponse(BaseModel):
    apple_code: str
    weight: int
    rotten: bool
    image_class: str
    quality: str


class StockStatusResponse(BaseModel):
    special: int
    good: int
    bad: int
    rotten: int
