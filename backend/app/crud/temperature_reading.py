import uuid
from sqlmodel import Session, select

from app.models.temperature_reading import (
    TemperatureReading,
    TemperatureReadingCreate,
    TemperatureReadingUpdate,
)


def create_temperature_reading(
    *, session: Session, temperature_reading_in: TemperatureReadingCreate
) -> TemperatureReading:
    db_obj = TemperatureReading.model_validate(temperature_reading_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_temperature_reading(
    *, session: Session, db_temperature_reading: TemperatureReading, temperature_reading_in: TemperatureReadingUpdate
) -> TemperatureReading:
    reading_data = temperature_reading_in.model_dump(exclude_unset=True)
    db_temperature_reading.sqlmodel_update(reading_data)
    session.add(db_temperature_reading)
    session.commit()
    session.refresh(db_temperature_reading)
    return db_temperature_reading


def get_temperature_reading_by_id(
    *, session: Session, temperature_reading_id: uuid.UUID
) -> TemperatureReading | None:
    return session.get(TemperatureReading, temperature_reading_id)


def get_temperature_readings_by_weather_station_id(
    *, session: Session, weather_station_id: uuid.UUID, skip: int = 0, limit: int = 1000
) -> list[TemperatureReading]:
    statement = select(TemperatureReading).where(TemperatureReading.weather_station_id == weather_station_id).offset(skip).limit(limit)
    return session.exec(statement).all()


def delete_temperature_reading(
    *, session: Session, temperature_reading: TemperatureReading
) -> TemperatureReading:
    session.delete(temperature_reading)
    session.commit()
    return temperature_reading
