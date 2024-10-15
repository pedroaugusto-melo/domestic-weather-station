import uuid
from sqlmodel import Session

from app.models.weather_station import (
    WeatherStation,
    WeatherStationCreate,
    WeatherStationUpdate,
)


def create_weather_station(
    *, session: Session, weather_station_in: WeatherStationCreate
) -> WeatherStation:
    db_obj = WeatherStation.model_validate(weather_station_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_weather_station(
    *, session: Session, db_weather_station: WeatherStation, weather_station_in: WeatherStationUpdate
) -> WeatherStation:
    station_data = weather_station_in.model_dump(exclude_unset=True)
    db_weather_station.sqlmodel_update(station_data)
    session.add(db_weather_station)
    session.commit()
    session.refresh(db_weather_station)
    return db_weather_station


def get_weather_station_by_id(
    *, session: Session, weather_station_id: uuid.UUID
) -> WeatherStation | None:
    return session.get(WeatherStation, weather_station_id)


def delete_weather_station(
    *, session: Session, weather_station: WeatherStation
) -> WeatherStation:
    session.delete(weather_station)
    session.commit()
    return weather_station
