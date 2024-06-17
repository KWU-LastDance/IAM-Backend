import random

from sqlalchemy.orm import Session

from app.repositories.monitoring_repository import MonitoringRepository
from app.schemas.monitoring_data import MonitoringDataCreate


class MonitoringService:
    def __init__(self, monitoring_repository: MonitoringRepository):
        self.monitoring_repository = monitoring_repository

    def get_now_data(self, raw: MonitoringDataCreate, db: Session):
        prev = self.monitoring_repository.get_by_time(raw.timestamp, db)
        if prev:
            return prev
        return self.monitoring_repository.create(raw, db)

    def get_all_datas(self, db: Session):
        return self.monitoring_repository.get_all(db)

    def get_temperature_datas(self, db: Session):
        return self.monitoring_repository.get_all_temperature(db)

    def get_humidity_datas(self, db: Session):
        return self.monitoring_repository.get_all_humidity(db)
