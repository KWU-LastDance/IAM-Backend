from datetime import datetime

import pytz
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from enum import Enum as PyEnum
from app.db.base import Base


class QualityEnum(PyEnum):
    special = 'special'
    good = 'good'
    bad = 'bad'
    none = None

class AppleClassification(Base):
    __tablename__ = 'apple_classification'

    id = Column(Integer, primary_key=True)
    apple_code = Column(String, index=True)
    weight = Column(Integer)
    rotten = Column(Boolean)
    image_class = Column(Enum(QualityEnum))
    quality = Column(Enum(QualityEnum))
    timestamp = Column(DateTime, default=datetime.now(tz=pytz.timezone('Asia/Seoul')).replace(microsecond=0))
