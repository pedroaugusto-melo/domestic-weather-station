from sqlmodel import Session
import uuid

from app.models.weather_station_model import WeatherStationModel, WeatherStationModelCreate, WeatherStationModelUpdate

import app.crud.weather_station_model as crud
import app.service.microcontroller as microcontroller_service


def get_weather_station_model_by_id(session: Session, id: uuid.UUID) -> WeatherStationModel | None:
    return crud.get_weather_station_model_by_id(session=session, weather_station_model_id=id)


def create_weather_station_model(session: Session, weather_station_model_in: WeatherStationModelCreate) -> WeatherStationModel:
    microcontroller = microcontroller_service.get_microcontroller_by_id(session=session, microcontroller_id=weather_station_model_in.microcontroller_id)

    if microcontroller is None:
        raise ValueError(f"Microcontroller with id {weather_station_model_in.microcontroller_id} not found")

    return crud.create_weather_station_model(session=session, weather_station_model_in=weather_station_model_in)


def update_weather_station_model(session: Session, id: uuid.UUID, weather_station_model_in: WeatherStationModelUpdate) -> WeatherStationModel | None:
    weather_station = get_weather_station_model_by_id(session=session, id=id)

    if weather_station is None:
        return None
    
    if weather_station_model_in.microcontroller_id:
        microcontroller = microcontroller_service.get_microcontroller_by_id(session=session, id=weather_station_model_in.microcontroller_id)

        if microcontroller is None:
            raise ValueError(f"Microcontroller with id {weather_station_model_in.microcontroller_id} not found")
    
    return crud.update_weather_station_model(session=session, db_weather_station_model=weather_station, weather_station_model_in=weather_station_model_in)


def delete_weather_station_model(session: Session, id: uuid.UUID) -> WeatherStationModel:
    weather_station = get_weather_station_model_by_id(session=session, id=id)

    if weather_station is None:
        return None
    
    return crud.delete_weather_station_model(session=session, weather_station_model=weather_station)