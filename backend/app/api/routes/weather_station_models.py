import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends

from app.api.deps.user import get_current_user
from app.api.deps.db import SessionDep
import app.api.deps.weather_station_model as deps

from app.models.weather_station_model import (
    WeatherStationModelCreate,
    WeatherStationModelUpdate,
    WeatherStationModelPublic,
)
from app.models.message import Message

import app.service.weather_station_model as service


router = APIRouter()


@router.get("/{id}", response_model=WeatherStationModelPublic, dependencies=[Depends(get_current_user)])
def read_weather_station_model(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get weather station model by ID.
    """

    weather_station_model = service.get_weather_station_model_by_id(
        session=session, id=id
    )

    if not weather_station_model:
        raise HTTPException(status_code=404, detail="Weather Station Model not found")
    
    return weather_station_model


@router.post("/", response_model=WeatherStationModelPublic, dependencies=[Depends(deps.authorize_create_weather_station_model)])
def create_weather_station_model(
    *, session: SessionDep, weather_station_model_in: WeatherStationModelCreate
) -> Any:
    """
    Create new weather station model.
    """
    
    try:
        weather_station_model = service.create_weather_station_model(
            session=session, weather_station_model_in=weather_station_model_in
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return weather_station_model


@router.put("/{id}", response_model=WeatherStationModelPublic, dependencies=[Depends(deps.authorize_update_weather_station_model)])
def update_weather_station_model(
    *,
    session: SessionDep,
    id: uuid.UUID,
    weather_station_model_in: WeatherStationModelUpdate,
) -> Any:
    """
    Update a weather station model.
    """
    
    try:
        updated_weather_station_model = service.update_weather_station_model(
            session=session, id=id, weather_station_model_in=weather_station_model_in
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if update_weather_station_model is None:
        raise HTTPException(status_code=404, detail="Weather Station Model not found")

    return updated_weather_station_model


@router.delete("/{id}", response_model=Message, dependencies=[Depends(deps.authorize_delete_weather_station_model)])
def delete_weather_station_model(
    *, session: SessionDep, id: uuid.UUID
) -> Message:
    """
    Delete a weather station model.
    """
    
    deleted_weather_station_model = service.delete_weather_station_model(
        session=session, id=id
    )

    if deleted_weather_station_model is None:
        raise HTTPException(status_code=404, detail="Weather Station Model not found")
    
    return Message(message="Weather Station Model deleted successfully")
