import uuid
from typing import Any, Annotated
from sqlalchemy.exc import IntegrityError

from fastapi import APIRouter, HTTPException, Depends

from app.api.deps.db import SessionDep
import app.api.deps.weather_station as deps
from app.api.deps.user import get_current_user, CurrentUser

from app.models.weather_station import (
    WeatherStationCreate,
    WeatherStationUpdate,
    WeatherStationPublic,
)
from app.models.message import Message

import app.service.weather_station as service


router = APIRouter()


@router.get("/{id}", response_model=WeatherStationPublic, dependencies=[Depends(deps.authorize_read_weather_station)])
def read_weather_station(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get weather station by ID.
    """

    weather_station = service.get_weather_station_by_id(
        session=session, id=id
    )
    
    return weather_station


@router.post("/", response_model=WeatherStationPublic, dependencies=[Depends(deps.authorize_create_weather_station)])
def create_weather_station(
    *, session: SessionDep, weather_station_in: WeatherStationCreate
) -> Any:
    """
    Create new weather station.
    """
    
    try:
        created_weather_station = service.create_weather_station(session=session, weather_station_in=weather_station_in)
    except (ValueError, IntegrityError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    return created_weather_station


@router.put("/{id}", response_model=WeatherStationPublic, dependencies=[Depends(deps.authorize_update_weather_station)])
def update_weather_station(
    *,
    session: SessionDep,
    id: uuid.UUID,
    weather_station_in: WeatherStationUpdate,
) -> Any:
    """
    Update a weather station.
    """
    
    try:
        updated_weather_station = service.update_weather_station(session=session, id=id, weather_station_in=weather_station_in)
    except (ValueError, IntegrityError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    if update_weather_station is None:
            raise HTTPException(status_code=404, detail="Weather Station not found")
    
    return updated_weather_station


@router.delete("/{id}", response_model=Message, dependencies=[Depends(deps.authorize_delete_weather_station)])
def delete_weather_station(
    *, session: SessionDep, id: uuid.UUID
) -> Message:
    """
    Delete a weather station.
    """
    
    weather_station = service.delete_weather_station(session=session, id=id)

    if weather_station is None:
        raise HTTPException(status_code=404, detail="Weather Station not found")
    
    return Message(message="Weather Station deleted successfully")


@router.get("/", response_model=list[WeatherStationPublic])
def list_weather_stations(
    session: SessionDep,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get list of weather stations.
    For regular users: returns only their weather stations
    For superusers: returns all weather stations
    """
    if current_user.is_superuser:
        weather_stations = service.get_weather_stations(
            session=session, skip=skip, limit=limit
        )
    else:
        weather_stations = service.get_user_weather_stations(
            session=session, user_id=current_user.id, skip=skip, limit=limit
        )
    
    return weather_stations
