import uuid
from typing import Any, List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError

from app.api.deps.db import SessionDep
import app.api.deps.weather_station_model_sensor as deps

from app.models.weather_station_model_sensor import (
    WeatherStationModelSensorCreate,
    WeatherStationModelSensorUpdate,
    WeatherStationModelSensorPublic,
)
from app.models.message import Message

import app.service.weather_station_model_sensor as service


router = APIRouter()


@router.post("/", response_model=WeatherStationModelSensorPublic, dependencies=[Depends(deps.authorize_create_weather_station_model_sensor)])
def create_weather_station_model_sensor(
    *,
    session: SessionDep,
    wsms_in: WeatherStationModelSensorCreate
) -> Any:
    """
    Create a new association between Weather Station Model and Sensor.
    """
    try:
        wsms = service.create_weather_station_model_sensor(session=session, wsms_in=wsms_in)
    except (ValueError, IntegrityError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    return wsms


@router.get("/{id}", response_model=WeatherStationModelSensorPublic, dependencies=[Depends(deps.authorize_read_weather_station_model_sensor)])
def read_weather_station_model_sensor(
    *,
    session: SessionDep,
    id: uuid.UUID
) -> Any:
    """
    Get an association by ID.
    """

    wsms = service.get_weather_station_model_sensor_by_id(session=session, id=id)

    if wsms is None:
        raise HTTPException(status_code=404, detail="Weather station model sensor not found")
    
    return wsms


@router.get("/models/{model_id}", response_model=List[WeatherStationModelSensorPublic], dependencies=[Depends(deps.authorize_read_weather_station_model_sensor)])
def read_associations_by_model_id(
    *,
    session: SessionDep,
    model_id: uuid.UUID
) -> Any:
    """
    Get associations by Weather Station Model ID.
    """

    wsms_list = service.get_weather_station_model_sensor_by_model_id(
        session=session, model_id=model_id
    )

    return wsms_list


@router.get("/sensors/{sensor_id}", response_model=List[WeatherStationModelSensorPublic], dependencies=[Depends(deps.authorize_read_weather_station_model_sensor)])
def read_associations_by_sensor_id(
    *,
    session: SessionDep,
    sensor_id: uuid.UUID
) -> Any:
    """
    Get associations by Sensor ID.
    """

    wsms_list = service.get_weather_station_model_sensor_by_sensor_id(
        session=session, sensor_id=sensor_id
    )

    return wsms_list


@router.put("/{id}", response_model=WeatherStationModelSensorPublic, dependencies=[Depends(deps.authorize_update_weather_station_model_sensor)])
def update_weather_station_model_sensor(
    *,
    session: SessionDep,
    id: uuid.UUID,
    wsms_in: WeatherStationModelSensorUpdate
) -> Any:
    """
    Update an association by ID.
    """

    try:
        wsms = service.update_weather_station_model_sensor(session=session, id=id, wsms_in=wsms_in)
    except (ValueError, IntegrityError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    if wsms is None:
        raise HTTPException(status_code=404, detail="Weather station model sensor not found")

    return wsms


@router.delete("/{id}", response_model=Message, dependencies=[Depends(deps.authorize_delete_weather_station_model_sensor)])
def delete_weather_station_model_sensor(
    *,
    session: SessionDep,
    id: uuid.UUID
) -> Any:
    """
    Delete an association by ID.
    """
    
    wsms = service.delete_weather_station_model_sensor(session=session, id=id)

    if wsms is None:
        raise HTTPException(status_code=404, detail="Weather station model sensor not found")
    
    return Message(message="Weather station model sensor deleted successfully")
