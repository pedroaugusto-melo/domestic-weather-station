import uuid
from typing import Any, List

from fastapi import APIRouter, HTTPException, Depends

from app.api.deps import SessionDep, CurrentUser, get_current_user

from app.models.weather_station_model_sensor import (
    WeatherStationModelSensorCreate,
    WeatherStationModelSensorUpdate,
    WeatherStationModelSensorPublic,
)
from app.models.message import Message

import app.crud.weather_station_model_sensor as crud


router = APIRouter()


@router.post("/", response_model=WeatherStationModelSensorPublic)
def create_weather_station_model_sensor(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    wsms_in: WeatherStationModelSensorCreate
) -> Any:
    """
    Create a new association between Weather Station Model and Sensor.
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    wsms = crud.create_weather_station_model_sensor(session=session, wsms_in=wsms_in)
    return wsms


@router.get("/{id}", response_model=WeatherStationModelSensorPublic, dependencies=[Depends(get_current_user)])
def read_weather_station_model_sensor(
    *,
    session: SessionDep,
    id: uuid.UUID
) -> Any:
    """
    Get an association by ID.
    """

    wsms = crud.get_weather_station_model_sensor_by_id(session=session, id=id)

    if not wsms:
        raise HTTPException(status_code=404, detail="Association not found")
    
    return wsms


@router.get("/model/{model_id}", response_model=List[WeatherStationModelSensorPublic], dependencies=[Depends(get_current_user)])
def read_associations_by_model_id(
    *,
    session: SessionDep,
    model_id: uuid.UUID
) -> Any:
    """
    Get associations by Weather Station Model ID.
    """

    wsms_list = crud.get_weather_station_model_sensors_by_model_id(
        session=session, weather_station_model_id=model_id
    )

    return wsms_list


@router.get("/sensor/{sensor_id}", response_model=List[WeatherStationModelSensorPublic], dependencies=[Depends(get_current_user)])
def read_associations_by_sensor_id(
    *,
    session: SessionDep,
    sensor_id: uuid.UUID
) -> Any:
    """
    Get associations by Sensor ID.
    """

    wsms_list = crud.get_weather_station_model_sensors_by_sensor_id(
        session=session, sensor_id=sensor_id
    )
    return wsms_list


@router.put("/{id}", response_model=WeatherStationModelSensorPublic)
def update_weather_station_model_sensor(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    wsms_in: WeatherStationModelSensorUpdate
) -> Any:
    """
    Update an association by ID.
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    wsms = crud.get_weather_station_model_sensor_by_id(session=session, id=id)
    
    if not wsms:
        raise HTTPException(status_code=404, detail="Association not found")
    wsms = crud.update_weather_station_model_sensor(
        session=session, db_obj=wsms, obj_in=wsms_in
    )
    
    return wsms


@router.delete("/{id}", response_model=Message)
def delete_weather_station_model_sensor(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID
) -> Any:
    """
    Delete an association by ID.
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    wsms = crud.get_weather_station_model_sensor_by_id(session=session, id=id)

    if not wsms:
        raise HTTPException(status_code=404, detail="Association not found")
    
    crud.delete_weather_station_model_sensor(session=session, id=id)
    return Message(message="Association deleted successfully")
