import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends

from app.api.deps import CurrentUser, SessionDep, get_current_user

from app.models.temperature_reading import (
    TemperatureReadingCreate,
    TemperatureReadingUpdate,
    TemperatureReadingPublic,
)
from app.models.message import Message

import app.crud.temperature_reading as crud


router = APIRouter()


@router.get("/{id}", response_model=TemperatureReadingPublic, dependencies=[Depends(get_current_user)])
def read_temperature_reading(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get temperature reading by ID.
    """

    temperature_reading = crud.get_temperature_reading_by_id(
        session=session, temperature_reading_id=id
    )

    if not temperature_reading:
        raise HTTPException(status_code=404, detail="Temperature Reading not found")
    
    return temperature_reading


@router.post("/", response_model=TemperatureReadingPublic)
def create_temperature_reading(
    *, session: SessionDep, current_user: CurrentUser, temperature_reading_in: TemperatureReadingCreate
) -> Any:
    """
    Create new temperature reading.
    """

    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    temperature_reading = crud.create_temperature_reading(
        session=session, temperature_reading_in=temperature_reading_in
    )
    return temperature_reading


@router.put("/{id}", response_model=TemperatureReadingPublic)
def update_temperature_reading(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    temperature_reading_in: TemperatureReadingUpdate,
) -> Any:
    """
    Update a temperature reading.
    """

    temperature_reading = crud.get_temperature_reading_by_id(
        session=session, temperature_reading_id=id
    )
    
    if not temperature_reading:
        raise HTTPException(status_code=404, detail="Temperature Reading not found")
    
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    updated_temperature_reading = crud.update_temperature_reading(
        session=session,
        db_temperature_reading=temperature_reading,
        temperature_reading_in=temperature_reading_in,
    )
    return updated_temperature_reading

@router.delete("/{id}")
def delete_temperature_reading(
    *, session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a temperature reading.
    """

    temperature_reading = crud.get_temperature_reading_by_id(
        session=session, temperature_reading_id=id
    )
    
    if not temperature_reading:
        raise HTTPException(status_code=404, detail="Temperature Reading not found")
    
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    crud.delete_temperature_reading(
        session=session, temperature_reading=temperature_reading
    )
    return Message(message="Temperature Reading deleted successfully")
