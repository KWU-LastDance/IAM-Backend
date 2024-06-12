import datetime

from sqlalchemy.orm import Session

from app.schemas.monitoring_data import MonitoringDataCreate
from app.models.monitoring_data import MonitoringData


class MonitoringRepository:
    def create(self, monitoring: MonitoringDataCreate, db: Session):
        monitoring_data = monitoring.dict(exclude_unset=True)
        db_monitoring = MonitoringData(**monitoring_data)
        db.add(db_monitoring)
        db.commit()
        db.refresh(db_monitoring)
        return db_monitoring

    def get_by_time(self, time: datetime.datetime, db: Session):
        return db.query(MonitoringData).filter(MonitoringData.timestamp == time).first()

    def get_all(self, db: Session):
        return db.query(MonitoringData).all()

    def get_all_temperature(self, db: Session):
        return db.query(MonitoringData).filter(MonitoringData.temperature != None).all()

    def get_all_humidity(self, db: Session):
        return db.query(MonitoringData).filter(MonitoringData.humidity != None).all()
