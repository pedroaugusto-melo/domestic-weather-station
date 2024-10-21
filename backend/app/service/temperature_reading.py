from sqlmodel import Session
import uuid

from app.models.temperature_reading import TemperatureReading, TemperatureReadingCreate, TemperatureReadingUpdate

import app.crud.temperature_reading as crud

import app.service.sensor as sensor_service
import app.service.weather_station as weather_station_service


def get_temperature_reading_by_id(session: Session, id: uuid.UUID) -> TemperatureReading | None:
    return crud.get_temperature_reading_by_id(session=session, temperature_reading_id=id)


def get_temperature_readings_by_weather_station_id(session: Session, weather_station_id: uuid.UUID, skip: int = 0, limit: int = 1000) -> list[TemperatureReading]:
    return crud.get_temperature_readings_by_weather_station_id(session=session, weather_station_id=weather_station_id, skip=skip, limit=limit)


def create_temperature_reading(session: Session, temperature_reading_in: TemperatureReadingCreate) -> TemperatureReading:
    sensor = sensor_service.get_sensor_by_id(session=session, id=temperature_reading_in.sensor_id)

    if sensor is None:
        raise ValueError(f"Sensor with ID {temperature_reading_in.sensor_id} not found")
    
    weather_station = weather_station_service.get_weather_station_by_id(session=session, id=temperature_reading_in.weather_station_id)
    
    if weather_station is None:
        raise ValueError(f"Weather Station with ID {temperature_reading_in.weather_station_id} not found")
    
    return crud.create_temperature_reading(session=session, temperature_reading_in=temperature_reading_in)


def update_temperature_reading(session: Session, id: uuid.UUID, temperature_reading_in: TemperatureReadingUpdate) -> TemperatureReading | None:
    temperature_reading = get_temperature_reading_by_id(session=session, id=id)
    
    if temperature_reading is None:
        return None
    
    if temperature_reading_in.sensor_id:
        sensor = sensor_service.get_sensor_by_id(session=session, id=temperature_reading_in.sensor_id)
        
        if sensor is None:
            raise ValueError(f"Sensor with ID {temperature_reading_in.sensor_id} not found")
    
    if temperature_reading_in.weather_station_id:
        weather_station = weather_station_service.get_weather_station_by_id(session=session, weather_station_id=temperature_reading_in.weather_station_id)
        
        if weather_station is None:
            raise ValueError(f"Weather Station with ID {temperature_reading_in.weather_station_id} not found")
    
    return crud.update_temperature_reading(session=session, db_temperature_reading=temperature_reading, temperature_reading_in=temperature_reading_in)


def delete_temperature_reading(session: Session, id: uuid.UUID) -> TemperatureReading | None:
    temperature_reading = get_temperature_reading_by_id(session=session, id=id)
    
    if temperature_reading is None:
        return None
    
    return crud.delete_temperature_reading(session=session, temperature_reading=temperature_reading)