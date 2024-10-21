from sqlmodel import Session
import uuid

from app.constants.data_reading_types import (
    ReadingTypes,
    DataReadingTypesClasses,
    DataReadingCreateTypesClasses,
    DataReadingUpdateTypesClasses
)

import app.crud.data_reading as crud

import app.service.sensor as sensor_service
import app.service.weather_station as weather_station_service



def get_data_reading_by_id(session: Session, id: uuid.UUID, reading_type: ReadingTypes) -> DataReadingTypesClasses | None:
    return crud.get_data_reading_by_id(session=session, data_reading_id=id, reading_type=reading_type)


def get_data_readings_by_weather_station_id(session: Session, weather_station_id: uuid.UUID, reading_type: ReadingTypes, skip: int = 0, limit: int = 1000) -> list[DataReadingTypesClasses]:
    return crud.get_data_readings_by_weather_station_id(session=session, weather_station_id=weather_station_id, skip=skip, limit=limit, reading_type=reading_type)


def create_data_reading(session: Session, data_reading_in: DataReadingCreateTypesClasses, reading_type: ReadingTypes) -> DataReadingTypesClasses | None:
    sensor = sensor_service.get_sensor_by_id(session=session, id=data_reading_in.sensor_id)

    if sensor is None:
        raise ValueError(f"Sensor with ID {data_reading_in.sensor_id} not found")
    
    weather_station = weather_station_service.get_weather_station_by_id(session=session, id=data_reading_in.weather_station_id)
    
    if weather_station is None:
        raise ValueError(f"Weather Station with ID {data_reading_in.weather_station_id} not found")
    
    return crud.create_data_reading(session=session, data_reading_in=data_reading_in, reading_type=reading_type)


def update_data_reading(session: Session, id: uuid.UUID, data_reading_in: DataReadingUpdateTypesClasses, reading_type: ReadingTypes) -> DataReadingTypesClasses | None:
    data_reading = get_data_reading_by_id(session=session, id=id, reading_type=reading_type)
    
    if data_reading is None:
        return None
    
    if data_reading.sensor_id:
        sensor = sensor_service.get_sensor_by_id(session=session, id=data_reading.sensor_id)
        
        if sensor is None:
            raise ValueError(f"Sensor with ID {data_reading.sensor_id} not found")
    
    if data_reading.weather_station_id:
        weather_station = weather_station_service.get_weather_station_by_id(session=session, weather_station_id=data_reading.weather_station_id)
        
        if weather_station is None:
            raise ValueError(f"Weather Station with ID {data_reading.weather_station_id} not found")
    
    return crud.update_data_reading(session=session, db_data_reading=data_reading, data_reading_in=data_reading_in)


def delete_data_reading(session: Session, id: uuid.UUID, reading_type: ReadingTypes) -> DataReadingTypesClasses | None:
    data_reading = get_data_reading_by_id(session=session, id=id , reading_type=reading_type)
    
    if data_reading is None:
        return None
    
    return crud.delete_data_reading(session=session, data_reading=data_reading)