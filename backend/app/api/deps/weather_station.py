from fastapi import HTTPException
from sqlmodel import Session
import uuid

from app.api.deps.user import CurrentUser
from app.api.deps.db import SessionDep

from app.models.weather_station import WeatherStationCreate, WeatherStationUpdate

import app.service.weather_station as service


def authorize_read_weather_station(id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> None:
    weather_station = service.get_weather_station_by_id(id=id, session=session)

    if not weather_station:
        raise HTTPException(status_code=404, detail="Weather Station not found")

    if not current_user.is_superuser and weather_station.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions to read weather station")


def authorize_create_weather_station(current_user: CurrentUser, weather_station_in: WeatherStationCreate) -> None:
    if not current_user.is_superuser and weather_station_in.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions to create weather station")


def authorize_update_weather_station(id: uuid.UUID, current_user: CurrentUser, weather_station_in: WeatherStationUpdate, session: SessionDep) -> None:
    authorize_read_weather_station(id=id, current_user=current_user, session=session)

    if not current_user.is_superuser and weather_station_in.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions to update weather station")


def authorize_delete_weather_station(id: uuid.UUID, current_user: CurrentUser, session: SessionDep) -> None:
    authorize_read_weather_station(id=id, current_user=current_user, session=session)