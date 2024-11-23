import uuid
from sqlmodel import Session, select

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


def get_weather_station_by_part_number(
    *, session: Session, part_number: str
) -> WeatherStation | None:
    statement = select(WeatherStation).where(WeatherStation.part_number == part_number)
    weather_station = session.exec(statement).first()
    return weather_station


def delete_weather_station(
    *, session: Session, weather_station: WeatherStation
) -> WeatherStation:
    session.delete(weather_station)
    session.commit()
    return weather_station


def get_weather_stations(*, session: Session, skip: int = 0, limit: int = 100) -> list[WeatherStation]:
    statement = select(WeatherStation).offset(skip).limit(limit)
    return session.exec(statement).all()


def get_user_weather_stations(*, session: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[WeatherStation]:
    statement = select(WeatherStation).where(WeatherStation.user_id == user_id).offset(skip).limit(limit)
    return session.exec(statement).all()
