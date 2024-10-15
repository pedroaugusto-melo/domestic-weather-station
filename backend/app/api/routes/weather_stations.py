import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends

from app.api.deps import CurrentUser, SessionDep, get_current_user

from app.models.weather_station import (
    WeatherStationCreate,
    WeatherStationUpdate,
    WeatherStationPublic,
)
from app.models.message import Message

import app.crud.weather_station as crud


router = APIRouter()


@router.get("/{id}", response_model=WeatherStationPublic, dependencies=[Depends(get_current_user)])
def read_weather_station(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get weather station by ID.
    """

    weather_station = crud.get_weather_station_by_id(
        session=session, weather_station_id=id
    )

    if not weather_station:
        raise HTTPException(status_code=404, detail="Weather Station not found")
    
    return weather_station


@router.post("/", response_model=WeatherStationPublic)
def create_weather_station(
    *, session: SessionDep, current_user: CurrentUser, weather_station_in: WeatherStationCreate
) -> Any:
    """
    Create new weather station.
    """

    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    if not current_user.is_superuser:
        weather_station_in.user_id = current_user.id
    
    weather_station = crud.create_weather_station(
        session=session, weather_station_in=weather_station_in
    )
    return weather_station


@router.put("/{id}", response_model=WeatherStationPublic)
def update_weather_station(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    weather_station_in: WeatherStationUpdate,
) -> Any:
    """
    Update a weather station.
    """

    weather_station = crud.get_weather_station_by_id(
        session=session, weather_station_id=id
    )
    
    if not weather_station:
        raise HTTPException(status_code=404, detail="Weather Station not found")
    
    if not current_user.is_superuser and weather_station.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    updated_weather_station = crud.update_weather_station(
        session=session,
        db_weather_station=weather_station,
        weather_station_in=weather_station_in,
    )
    return updated_weather_station


@router.delete("/{id}")
def delete_weather_station(
    *, session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a weather station.
    """
    
    weather_station = crud.get_weather_station_by_id(
        session=session, weather_station_id=id
    )
    
    if not weather_station:
        raise HTTPException(status_code=404, detail="Weather Station not found")
    
    if not current_user.is_superuser and weather_station.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    crud.delete_weather_station(
        session=session, weather_station=weather_station
    )
    return Message(message="Weather Station deleted successfully")
