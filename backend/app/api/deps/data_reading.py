from fastapi import HTTPException
import uuid

from app.api.deps.user import CurrentUser
from app.api.deps.db import SessionDep
from app.constants.reading_types import ReadingTypes

import app.service.data_reading as service
import app.service.weather_station as weather_station_service


def authorize_read_data_reading(current_user: CurrentUser, session: SessionDep, id: uuid.UUID, reading_type: ReadingTypes) -> None:
    data_reading = service.get_data_reading_by_id(session=session, id=id, reading_type=reading_type)

    if not data_reading:
        raise HTTPException(status_code=404, detail="Data reading not found")
    
    weather_station = weather_station_service.get_weather_station_by_id(session=session, id=data_reading.weather_station_id)
    
    if not current_user.is_superuser and weather_station.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to read this data reading")


def authorize_read_weather_station_data_readings(current_user: CurrentUser, session: SessionDep, id: uuid.UUID) -> None:
    weather_station = weather_station_service.get_weather_station_by_id(session=session, id=id)

    if not weather_station:
        raise HTTPException(status_code=404, detail="Weather station not found")
    
    if not current_user.is_superuser and weather_station.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to read data readings from this weather station")


def authorize_delete_data_reading(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions to delete a data reading")