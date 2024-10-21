from sqlmodel import Session
import uuid

from app.models.weather_station_model_sensor import WeatherStationModelSensor, WeatherStationModelSensorCreate, WeatherStationModelSensorUpdate

import app.crud.weather_station_model_sensor as crud

import app.service.weather_station_model as weather_station_model_service
import app.service.sensor as sensor_service


def get_weather_station_model_sensor_by_id(session: Session, id: uuid.UUID) -> WeatherStationModelSensor | None:
    return crud.get_weather_station_model_sensor_by_id(session=session, id=id)


def get_weather_station_model_sensor_by_model_id(session: Session, model_id: uuid.UUID) -> list[WeatherStationModelSensor]:
    return crud.get_weather_station_model_sensors_by_model_id(session=session, weather_station_model_id=model_id)


def get_weather_station_model_sensor_by_sensor_id(session: Session, sensor_id: uuid.UUID) -> list[WeatherStationModelSensor]:
    return crud.get_weather_station_model_sensors_by_sensor_id(session=session, sensor_id=sensor_id)


def create_weather_station_model_sensor(session: Session, wsms_in: WeatherStationModelSensorCreate) -> WeatherStationModelSensor:
    weather_station_model = weather_station_model_service.get_weather_station_model_by_id(session=session, id=wsms_in.weather_station_model_id)
    
    if weather_station_model is None:
        raise ValueError(f"Weather Station Model with ID {wsms_in.weather_station_model_id} not found")
    
    sensor = sensor_service.get_sensor_by_id(session=session, id=wsms_in.sensor_id)

    if sensor is None:
        raise ValueError(f"Sensor with ID {wsms_in.sensor_id} not found")

    return crud.create_weather_station_model_sensor(session=session, wsms_in=wsms_in)


def update_weather_station_model_sensor(session: Session, id: uuid.UUID, wsms_in: WeatherStationModelSensorUpdate) -> WeatherStationModelSensor | None:
    wsms = get_weather_station_model_sensor_by_id(session=session, id=id)

    if wsms is None:
        return None
    
    if wsms_in.weather_station_model_id:
        weather_station_model = weather_station_model_service.get_weather_station_model_by_id(session=session, id=wsms_in.weather_station_model_id)
        
        if weather_station_model is None:
            raise ValueError(f"Weather Station Model with ID {wsms_in.weather_station_model_id} not found")

    if wsms_in.sensor_id:
        sensor = sensor_service.get_sensor_by_id(session=session, id=wsms_in.sensor_id)

        if sensor is None:
            raise ValueError(f"Sensor with ID {wsms_in.sensor_id} not found")
        
    return crud.update_weather_station_model_sensor(session=session, wsms=wsms, wsms_in=wsms_in)


def delete_weather_station_model_sensor(session: Session, id: uuid.UUID) -> WeatherStationModelSensor | None:
    wsms = get_weather_station_model_sensor_by_id(session=session, id=id)

    if wsms is None:
        return None

    return crud.delete_weather_station_model_sensor(session=session, id=id)