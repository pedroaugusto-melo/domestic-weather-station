import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends

from app.api.deps import CurrentUser, SessionDep

from app.models.sensor import SensorCreate, SensorUpdate, SensorPublic
from app.models.message import Message

import app.crud.sensor as crud


router = APIRouter()


@router.get("/{id}", response_model=SensorPublic, dependencies=[Depends(CurrentUser)])
def read_sensor(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get sensor by ID.
    """
    sensor = crud.get_sensor_by_id(session=session, sensor_id=id)

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    return sensor


@router.post("/", response_model=SensorPublic)
def create_sensor(
    *, session: SessionDep, current_user: CurrentUser, sensor_in: SensorCreate
) -> Any:
    """
    Create new sensor.
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    sensor = crud.create_sensor(session=session, sensor_in=sensor_in)
    return sensor


@router.put("/{id}", response_model=SensorPublic)
def update_sensor(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    sensor_in: SensorUpdate,
) -> Any:
    """
    Update an sensor.
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    sensor = crud.get_sensor_by_id(session=session, item_id=id)
    
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    update_sensor = crud.update_sensor(session=session, db_sensor=sensor_in, item_in=sensor_in)
    return update_sensor


@router.delete("/{id}")
def delete_sensor(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an sensor.
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    sensor = crud.get_sensor_by_id(session=session, item_id=id)
    
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    crud.delete_sensor(session=session, sensor=sensor)

    return Message(message="Sensor deleted successfully")
