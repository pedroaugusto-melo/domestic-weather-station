import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends

from app.api.deps.db import SessionDep
import app.api.deps.data_reading as deps

from app.constants.reading_types import ReadingTypes

from app.models.temperature_reading import TemperatureReadingPublic
from app.models.gas_level_reading import GasLevelReadingPublic
from app.models.message import Message

import app.service.data_reading as service


router = APIRouter()


@router.get("/{id}", response_model=TemperatureReadingPublic | GasLevelReadingPublic, dependencies=[Depends(deps.authorize_read_data_reading)])
def read_data_reading(session: SessionDep, id: uuid.UUID, type: ReadingTypes) -> Any:
    """
    Get data reading by ID.
    """

    data_reading = service.get_data_reading_by_id(
        session=session, id=id, reading_type=type
    )

    if not data_reading:
        raise HTTPException(status_code=404, detail="Data Reading not found")
    
    return data_reading


@router.get("/weather-stations/{id}", response_model=list[TemperatureReadingPublic | GasLevelReadingPublic], dependencies=[Depends(deps.authorize_read_weather_station_data_readings)])
def read_weather_station_data_readings(session: SessionDep, id: uuid.UUID, type: ReadingTypes, skip: int = 0, limit: int = 1000) -> Any:
    """
    Get data readings by Weather Station ID.
    """

    data_readings = service.get_data_readings_by_weather_station_id(
        session=session, weather_station_id=id, skip=skip, limit=limit, reading_type=type
    )

    return data_readings


@router.delete("/{id}", response_model=Message, dependencies=[Depends(deps.authorize_delete_data_reading)])
def delete_data_reading(
    *, session: SessionDep, id: uuid.UUID, type: ReadingTypes
) -> Message:
    """
    Delete a data reading.
    """

    data_reading = service.delete_data_reading(
        session=session, id=id, reading_type=type
    )
    
    if not data_reading:
        raise HTTPException(status_code=404, detail="Data Reading not found")
    
    return Message(message="Data reading deleted successfully")
