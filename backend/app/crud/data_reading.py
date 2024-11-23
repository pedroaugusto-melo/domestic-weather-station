import uuid
from datetime import datetime, timedelta, UTC
from sqlmodel import Session, select

from app.constants.data_reading_types import ReadingTypes

from app.constants.data_reading_types import (
    ReadingClassesByType, 
    DataReadingTypesClasses, 
    DataReadingCreateTypesClasses, 
    DataReadingUpdateTypesClasses
)


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
    *, 
    session: Session, 
    weather_station_id: uuid.UUID, 
    minutes: int | None = None,
    skip: int = 0, 
    limit: int = 1000, 
    reading_type: ReadingTypes,
    order: str = 'desc',
    order_by: str = 'read_at'
) -> list[DataReadingTypesClasses]:
    ReadingClass = ReadingClassesByType[reading_type]
    
    # Get the column to order by
    order_column = getattr(ReadingClass, order_by)
    
    # Apply ordering
    if order.lower() == 'desc':
        order_column = order_column.desc()
    else:
        order_column = order_column.asc()
    
    # Start building the base query
    statement = (
        select(ReadingClass)
        .where(ReadingClass.weather_station_id == weather_station_id)
    )
    
    # Add time filter only if minutes parameter is provided
    if minutes is not None:
        time_threshold = datetime.now(UTC) - timedelta(minutes=minutes)
        statement = statement.where(ReadingClass.read_at >= time_threshold)
    
    # Add ordering, offset and limit
    statement = (
        statement
        .order_by(order_column)
        .offset(skip)
        .limit(limit)
    )

    return session.exec(statement).all()


def delete_data_reading(
    *, session: Session, data_reading: DataReadingTypesClasses
) -> DataReadingTypesClasses:
    session.delete(data_reading)
    session.commit()
    return data_reading
