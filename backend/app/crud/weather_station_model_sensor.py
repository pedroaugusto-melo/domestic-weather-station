import uuid
from typing import List, Optional
from sqlmodel import Session, select

from app.models.weather_station_model_sensor import (
    WeatherStationModelSensor,
    WeatherStationModelSensorCreate,
    WeatherStationModelSensorUpdate,
)


def create_weather_station_model_sensor(
    *, session: Session, wsms_in: WeatherStationModelSensorCreate
) -> WeatherStationModelSensor:
    db_obj = WeatherStationModelSensor.from_orm(wsms_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_weather_station_model_sensor_by_id(
    *, session: Session, id: uuid.UUID
) -> Optional[WeatherStationModelSensor]:
    return session.get(WeatherStationModelSensor, id)


def get_weather_station_model_sensors_by_model_id(
    *, session: Session, weather_station_model_id: uuid.UUID
) -> List[WeatherStationModelSensor]:
    statement = select(WeatherStationModelSensor).where(
        WeatherStationModelSensor.weather_station_model_id == weather_station_model_id
    )
    return session.exec(statement).all()


def get_weather_station_model_sensors_by_sensor_id(
    *, session: Session, sensor_id: uuid.UUID
) -> List[WeatherStationModelSensor]:
    statement = select(WeatherStationModelSensor).where(
        WeatherStationModelSensor.sensor_id == sensor_id
    )
    return session.exec(statement).all()


def update_weather_station_model_sensor(
    *, session: Session, wsms: WeatherStationModelSensor, wsms_in: WeatherStationModelSensorUpdate
) -> WeatherStationModelSensor:
    obj_data = wsms_in.dict(exclude_unset=True)
    for key, value in obj_data.items():
        setattr(wsms, key, value)
    session.add(wsms)
    session.commit()
    session.refresh(wsms)
    return wsms


def delete_weather_station_model_sensor(
    *, session: Session, id: uuid.UUID
) -> None:
    db_obj = session.get(WeatherStationModelSensor, id)
    if db_obj:
        session.delete(db_obj)
        session.commit()
