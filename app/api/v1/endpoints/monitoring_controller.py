import pytz
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from random import random
from datetime import datetime

from app.db.session import get_db
from app.repositories.monitoring_repository import MonitoringRepository
from app.schemas.monitoring_data import MonitoringDataCreate, CurrentDataResponse, TemperatureDataResponse, \
    HumidityDataResponse
from app.services.monitoring_service import MonitoringService

router = APIRouter()

monitoring_repository = MonitoringRepository()
monitoring_service = MonitoringService(monitoring_repository)


def create_data():
    temperature = 2 + round(random(), 3)
    humidity = 92 + round(random(), 3)
    timestamp = datetime.now().replace(microsecond=0)
    return temperature, humidity, timestamp


@router.get("/", response_model=list[CurrentDataResponse])
async def get_all(db: Session = Depends(get_db)):
    return monitoring_service.get_all_datas(db)


@router.get("/temperature", response_model=list[TemperatureDataResponse])
async def get_temperature(db: Session = Depends(get_db)):
    return monitoring_service.get_temperature_datas(db)


@router.get("/humidity", response_model=list[HumidityDataResponse])
async def get_humidity(db: Session = Depends(get_db)):
    return monitoring_service.get_humidity_datas(db)


@router.get("/now", response_model=CurrentDataResponse)
async def get_now(db: Session = Depends(get_db)):
    temperature, humidity, timestamp = create_data()
    raw_data = MonitoringDataCreate(
        temperature=temperature,
        humidity=humidity,
        timestamp=timestamp
    )
    return monitoring_service.get_now_data(raw_data, db)
