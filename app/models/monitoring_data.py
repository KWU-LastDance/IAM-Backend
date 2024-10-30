import datetime
from sqlalchemy import Column, Integer, Float, DateTime
from app.db.base import Base

class MonitoringData(Base):
    __tablename__ = 'monitoring_data'

    id = Column(Integer, primary_key=True)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)