import datetime
from pydantic import BaseModel, validator

class MonitoringDataBase(BaseModel):
    temperature: float
    humidity: float
    timestamp: datetime.datetime

    @validator("timestamp", pre=True, always=True)
    def remove_timezone(cls, v):
        return v.replace(tzinfo=None) if v.tzinfo else v

class MonitoringDataCreate(MonitoringDataBase):
    pass

class MonitoringData(MonitoringDataBase):
    id: int

    @validator("timestamp", pre=True, always=True)
    def remove_timezone(cls, v):
        return v.replace(tzinfo=None) if v.tzinfo else v

    class Config:
        from_attributes = True

class TemperatureDataResponse(BaseModel):
    id: int
    temperature: float
    timestamp: datetime.datetime

    @validator("timestamp", pre=True, always=True)
    def remove_timezone(cls, v):
        return v.replace(tzinfo=None) if v.tzinfo else v

    class Config:
        from_attributes = True

class HumidityDataResponse(BaseModel):
    id: int
    humidity: float
    timestamp: datetime.datetime

    @validator("timestamp", pre=True, always=True)
    def remove_timezone(cls, v):
        return v.replace(tzinfo=None) if v.tzinfo else v

    class Config:
        from_attributes = True

class CurrentDataResponse(BaseModel):
    temperature: float
    humidity: float
    timestamp: datetime.datetime

    @validator("timestamp", pre=True, always=True)
    def remove_timezone(cls, v):
        return v.replace(tzinfo=None) if v.tzinfo else v
