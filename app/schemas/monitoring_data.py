import datetime

from pydantic import BaseModel


class MonitoringDataBase(BaseModel):
    temperature: float
    humidity: float
    timestamp: datetime.datetime


class MonitoringDataCreate(MonitoringDataBase):
    pass


class MonitoringData(MonitoringDataBase):
    id: int
    timestamp: datetime.datetime

    class Config:
        from_attributes = True


class TemperatureDataResponse(BaseModel):
    id: int
    temperature: float
    timestamp: datetime.datetime

    class Config:
        from_attributes = True


class HumidityDataResponse(BaseModel):
    id: int
    humidity: float
    timestamp: datetime.datetime

    class Config:
        from_attributes = True


class CurrentDataResponse(BaseModel):
    temperature: float
    humidity: float
    timestamp: datetime.datetime
