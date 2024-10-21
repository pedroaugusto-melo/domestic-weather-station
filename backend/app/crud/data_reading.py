import uuid
from sqlmodel import Session, select

from app.constants.reading_types import ReadingTypes

from app.models.temperature_reading import (
    TemperatureReading,
    TemperatureReadingCreate,
    TemperatureReadingUpdate,
)
from app.models.gas_level_reading import (
    GasLevelReading,
    GasLevelReadingCreate,
    GasLevelReadingUpdate,
)


def create_data_reading(
    *, session: Session, data_reading_in: TemperatureReadingCreate | GasLevelReadingCreate, reading_type: ReadingTypes
) -> TemperatureReading | GasLevelReading:
    db_obj = None

    if reading_type == ReadingTypes.TEMPERATURE:
        db_obj = TemperatureReading.model_validate(data_reading_in)
    elif reading_type == ReadingTypes.GAS_LEVEL:
        db_obj = GasLevelReading.model_validate(data_reading_in)

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_data_reading(
    *, session: Session, db_data_reading: TemperatureReading | GasLevelReading, data_reading_in: TemperatureReadingUpdate | GasLevelReadingUpdate
) -> TemperatureReading | GasLevelReading:
    reading_data = data_reading_in.model_dump(exclude_unset=True)
    db_data_reading.sqlmodel_update(reading_data)
    session.add(db_data_reading)
    session.commit()
    session.refresh(db_data_reading)
    return db_data_reading


def get_data_reading_by_id(
    *, session: Session, data_reading_id: uuid.UUID, reading_type: ReadingTypes
) -> TemperatureReading | GasLevelReading | None:
    if reading_type == ReadingTypes.TEMPERATURE:
        return session.get(TemperatureReading, data_reading_id)
    elif reading_type == ReadingTypes.GAS_LEVEL:
        return session.get(GasLevelReading, data_reading_id)


def get_data_readings_by_weather_station_id(
    *, session: Session, weather_station_id: uuid.UUID, skip: int = 0, limit: int = 1000, reading_type: ReadingTypes
) -> list[TemperatureReading | GasLevelReading]:
    statement = select(TemperatureReading)

    if reading_type == ReadingTypes.TEMPERATURE:
        statement.where(TemperatureReading.weather_station_id == weather_station_id).offset(skip).limit(limit)
    elif reading_type == ReadingTypes.GAS_LEVEL:
        statement.where(GasLevelReading.weather_station_id == weather_station_id).offset(skip).limit(limit)

    return session.exec(statement).all()


def delete_data_reading(
    *, session: Session, data_reading: TemperatureReading | GasLevelReading
) -> TemperatureReading | GasLevelReading:
    session.delete(data_reading)
    session.commit()
    return data_reading
