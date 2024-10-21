import uuid
from sqlmodel import Session, select

from app.constants.reading_types import ReadingTypes

from app.models.temperature_reading import TemperatureReading, TemperatureReadingCreate, TemperatureReadingUpdate
from app.models.gas_level_reading import GasLevelReading, GasLevelReadingCreate, GasLevelReadingUpdate
from app.models.humidity_reading import HumidityReading, HumidityReadingCreate, HumidityReadingUpdate


DataReadingTypesClasses = TemperatureReading | GasLevelReading | HumidityReading
DataReadingCreateTypesClasses = TemperatureReadingCreate | GasLevelReadingCreate | HumidityReadingCreate
DataReadingUpdateTypesClasses = TemperatureReadingUpdate | GasLevelReadingUpdate | HumidityReadingUpdate


ReadingClassesByType = {
    ReadingTypes.TEMPERATURE: TemperatureReading,
    ReadingTypes.GAS_LEVEL: GasLevelReading,
    ReadingTypes.HUMIDITY: HumidityReading,
}


def create_data_reading(
    *, session: Session, data_reading_in: DataReadingCreateTypesClasses, reading_type: ReadingTypes
) -> DataReadingTypesClasses:
    db_obj = ReadingClassesByType[reading_type].model_validate(data_reading_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_data_reading(
    *, session: Session, db_data_reading: DataReadingTypesClasses, data_reading_in: DataReadingUpdateTypesClasses
) -> DataReadingCreateTypesClasses:
    reading_data = data_reading_in.model_dump(exclude_unset=True)
    db_data_reading.sqlmodel_update(reading_data)
    session.add(db_data_reading)
    session.commit()
    session.refresh(db_data_reading)
    return db_data_reading


def get_data_reading_by_id(
    *, session: Session, data_reading_id: uuid.UUID, reading_type: ReadingTypes
) -> DataReadingTypesClasses | None:
    return session.get(ReadingClassesByType[reading_type], data_reading_id)


def get_data_readings_by_weather_station_id(
    *, session: Session, weather_station_id: uuid.UUID, skip: int = 0, limit: int = 1000, reading_type: ReadingTypes
) -> list[DataReadingTypesClasses]:
    ReadingClass = ReadingClassesByType[reading_type]
    statement = select(ReadingClass).where(ReadingClass.weather_station_id == weather_station_id).offset(skip).limit(limit)

    return session.exec(statement).all()


def delete_data_reading(
    *, session: Session, data_reading: DataReadingTypesClasses
) -> DataReadingTypesClasses:
    session.delete(data_reading)
    session.commit()
    return data_reading
