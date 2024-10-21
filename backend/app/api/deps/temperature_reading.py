from fastapi import HTTPException
import uuid

from app.api.deps.user import CurrentUser
from app.api.deps.db import SessionDep

import app.service.temperature_reading as service
import app.service.weather_station as weather_station_service


def authorize_read_temperature_reading(current_user: CurrentUser, session: SessionDep, id: uuid.UUID ) -> None:
    temperature_reading = service.get_temperature_reading_by_id(session=session, id=id)

    if not temperature_reading:
        raise HTTPException(status_code=404, detail="Temperature reading not found")
    
    weather_station = weather_station_service.get_weather_station_by_id(session=session, id=temperature_reading.weather_station_id)
    
    if not current_user.is_superuser and weather_station.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to read this temperature reading")


def authorize_read_weather_station_temperature_readings(current_user: CurrentUser, session: SessionDep, id: uuid.UUID) -> None:
    weather_station = weather_station_service.get_weather_station_by_id(session=session, id=id)

    if not weather_station:
        raise HTTPException(status_code=404, detail="Weather station not found")
    
    if not current_user.is_superuser and weather_station.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions to read temperature readings from this weather station")


def authorize_delete_temperature_reading(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions to delete a temperature reading")