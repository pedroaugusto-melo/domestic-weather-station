import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends

from app.api.deps.db import SessionDep
import app.api.deps.temperature_reading as deps

from app.models.temperature_reading import TemperatureReadingPublic
from app.models.message import Message

import app.service.temperature_reading as service


router = APIRouter()


@router.get("/{id}", response_model=TemperatureReadingPublic, dependencies=[Depends(deps.authorize_read_temperature_reading)])
def read_temperature_reading(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get temperature reading by ID.
    """

    temperature_reading = service.get_temperature_reading_by_id(
        session=session, id=id
    )

    if not temperature_reading:
        raise HTTPException(status_code=404, detail="Temperature Reading not found")
    
    return temperature_reading


@router.get("/weather_stations/{id}", response_model=list[TemperatureReadingPublic], dependencies=[Depends(deps.authorize_read_weather_station_temperature_readings)])
def read_weather_station_temperature_readings(session: SessionDep, id: uuid.UUID, skip: int = 0, limit: int = 1000) -> Any:
    """
    Get temperature readings by Weather Station ID.
    """

    temperature_readings = service.get_temperature_readings_by_weather_station_id(
        session=session, weather_station_id=id, skip=skip, limit=limit
    )

    return temperature_readings


@router.delete("/{id}", response_model=Message, dependencies=[Depends(deps.authorize_delete_temperature_reading)])
def delete_temperature_reading(
    *, session: SessionDep, id: uuid.UUID
) -> Message:
    """
    Delete a temperature reading.
    """

    temperature_reading = service.delete_temperature_reading(
        session=session, id=id
    )
    
    if not temperature_reading:
        raise HTTPException(status_code=404, detail="Temperature Reading not found")
    
    return Message(message="Temperature Reading deleted successfully")
