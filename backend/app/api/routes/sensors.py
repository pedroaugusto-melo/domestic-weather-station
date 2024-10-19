import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends

from app.api.deps.user import get_current_user
from app.api.deps.db import SessionDep
import app.api.deps.sensor as deps

from app.models.sensor import SensorCreate, SensorUpdate, SensorPublic
from app.models.message import Message

import app.service.sensor as service


router = APIRouter()


@router.get("/{id}", response_model=SensorPublic, dependencies=[Depends(get_current_user)])
def read_sensor(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get sensor by ID.
    """

    sensor = service.get_sensor_by_id(session=session, sensor_id=id)

    if sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    return sensor


@router.post("/", response_model=SensorPublic, dependencies=[Depends(deps.authorize_create_sensor)])
def create_sensor(
    *, session: SessionDep, sensor_in: SensorCreate
) -> Any:
    """
    Create new sensor.
    """

    sensor = service.create_sensor(session=session, sensor_in=sensor_in)
    return sensor


@router.put("/{id}", response_model=SensorPublic, dependencies=[Depends(deps.authorize_update_sensor)])
def update_sensor(
    *,
    session: SessionDep,
    id: uuid.UUID,
    sensor_in: SensorUpdate,
) -> Any:
    """
    Update an sensor.
    """

    update_sensor = service.update_sensor(session=session, id=id, sensor_in=sensor_in)
    
    if update_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    return update_sensor


@router.delete("/{id}", response_model=Message, dependencies=[Depends(deps.authorize_delete_sensor)])
def delete_sensor(
    session: SessionDep, id: uuid.UUID
) -> Message:
    """
    Delete an sensor.
    """

    delete_sensor = service.delete_sensor(session=session, id=id)
    
    if not delete_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    return Message(message="Sensor deleted successfully")
