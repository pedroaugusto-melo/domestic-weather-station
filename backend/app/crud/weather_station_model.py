import uuid
from sqlmodel import Session

from app.models.weather_station_model import (
    WeatherStationModel,
    WeatherStationModelCreate,
    WeatherStationModelUpdate,
)


def create_weather_station_model(
    *, session: Session, weather_station_model_in: WeatherStationModelCreate
) -> WeatherStationModel:
    db_obj = WeatherStationModel.model_validate(weather_station_model_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_weather_station_model(
    *, session: Session, db_weather_station_model: WeatherStationModel, weather_station_model_in: WeatherStationModelUpdate
) -> WeatherStationModel:
    model_data = weather_station_model_in.model_dump(exclude_unset=True)
    db_weather_station_model.sqlmodel_update(model_data)
    session.add(db_weather_station_model)
    session.commit()
    session.refresh(db_weather_station_model)
    return db_weather_station_model


def get_weather_station_model_by_id(
    *, session: Session, weather_station_model_id: uuid.UUID
) -> WeatherStationModel | None:
    return session.get(WeatherStationModel, weather_station_model_id)


def delete_weather_station_model(
    *, session: Session, weather_station_model: WeatherStationModel
) -> WeatherStationModel:
    session.delete(weather_station_model)
    session.commit()
    return weather_station_model
