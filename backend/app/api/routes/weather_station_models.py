import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends

from app.api.deps.user import CurrentUser, get_current_user
from app.api.deps.db import SessionDep

from app.models.weather_station_model import (
    WeatherStationModelCreate,
    WeatherStationModelUpdate,
    WeatherStationModelPublic,
)
from app.models.message import Message

import app.crud.weather_station_model as crud


router = APIRouter()


@router.get("/{id}", response_model=WeatherStationModelPublic, dependencies=[Depends(get_current_user)])
def read_weather_station_model(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get weather station model by ID.
    """

    weather_station_model = crud.get_weather_station_model_by_id(
        session=session, weather_station_model_id=id
    )

    if not weather_station_model:
        raise HTTPException(status_code=404, detail="Weather Station Model not found")
    
    return weather_station_model


@router.post("/", response_model=WeatherStationModelPublic)
def create_weather_station_model(
    *, session: SessionDep, current_user: CurrentUser, weather_station_model_in: WeatherStationModelCreate
) -> Any:
    """
    Create new weather station model.
    """
    
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    weather_station_model = crud.create_weather_station_model(
        session=session, weather_station_model_in=weather_station_model_in
    )
    return weather_station_model


@router.put("/{id}", response_model=WeatherStationModelPublic)
def update_weather_station_model(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    weather_station_model_in: WeatherStationModelUpdate,
) -> Any:
    """
    Update a weather station model.
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    weather_station_model = crud.get_weather_station_model_by_id(
        session=session, weather_station_model_id=id
    )
    
    if not weather_station_model:
        raise HTTPException(status_code=404, detail="Weather Station Model not found")
    
    updated_weather_station_model = crud.update_weather_station_model(
        session=session,
        db_weather_station_model=weather_station_model,
        weather_station_model_in=weather_station_model_in,
    )
    return updated_weather_station_model


@router.delete("/{id}")
def delete_weather_station_model(
    *, session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a weather station model.
    """
    
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    weather_station_model = crud.get_weather_station_model_by_id(
        session=session, weather_station_model_id=id
    )
    
    if not weather_station_model:
        raise HTTPException(status_code=404, detail="Weather Station Model not found")
    
    crud.delete_weather_station_model(
        session=session, weather_station_model=weather_station_model
    )
    return Message(message="Weather Station Model deleted successfully")
