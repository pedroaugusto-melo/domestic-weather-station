from sqlmodel import Session
import uuid

import app.crud.weather_station as crud
from app.models.weather_station import WeatherStation, WeatherStationCreate, WeatherStationUpdate

import app.service.user as user_service
import app.service.weather_station_model as weather_station_model_service


def get_weather_station_by_id(session: Session, id: uuid.UUID) -> WeatherStation | None:
    return crud.get_weather_station_by_id(session=session, weather_station_id=id)


def get_weather_station_by_part_number(session: Session, part_number: str) -> WeatherStation | None:
    return crud.get_weather_station_by_part_number(session=session, part_number=part_number)


def create_weather_station(session: Session, weather_station_in: WeatherStationCreate) -> WeatherStation:
    user = user_service.get_user_by_id(session=session, id=weather_station_in.user_id)

    if user is None:
        raise ValueError(f"User with ID {weather_station_in.user_id} not found")
    
    weather_station_model = weather_station_model_service.get_weather_station_model_by_id(session=session, id=weather_station_in.weather_station_model_id)

    if weather_station_model is None:
        raise ValueError(f"Weather Station Model with ID {weather_station_in.weather_station_model_id} not found")
    
    return crud.create_weather_station(session=session, weather_station_in=weather_station_in)


def update_weather_station(session: Session, id: uuid.UUID, weather_station_in: WeatherStationUpdate) -> WeatherStation | None:
    weather_station = get_weather_station_by_id(session=session, id=id)

    if weather_station is None:
        return None

    if weather_station_in.user_id:
        user = user_service.get_user_by_id(session=session, user_id=weather_station_in.user_id)

        if user is None:
            raise ValueError(f"User with ID {weather_station_in.user_id} not found")
    
    if weather_station_in.weather_station_model_id:
        weather_station_model = weather_station_model_service.get_weather_station_model_by_id(session=session, id=weather_station_in.weather_station_model_id)

        if weather_station_model is None:
            raise ValueError(f"Weather Station Model with ID {weather_station_in.weather_station_model_id} not found")
    
    return crud.update_weather_station(session=session, db_weather_station=weather_station, weather_station_in=weather_station_in)


def delete_weather_station(session: Session, id: uuid.UUID) -> WeatherStation | None:
    weather_station = get_weather_station_by_id(session=session, id=id)

    if weather_station is None:
        return None

    return crud.delete_weather_station(session=session, weather_station=weather_station)


def get_weather_stations(session: Session, skip: int = 0, limit: int = 100) -> list[WeatherStation]:
    return crud.get_weather_stations(session=session, skip=skip, limit=limit)


def get_user_weather_stations(session: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[WeatherStation]:
    return crud.get_user_weather_stations(session=session, user_id=user_id, skip=skip, limit=limit)