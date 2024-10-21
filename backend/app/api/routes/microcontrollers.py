import uuid
from typing import Any
from sqlalchemy.exc import IntegrityError

from fastapi import APIRouter, HTTPException, Depends

from app.api.deps.user import get_current_user
from app.api.deps.db import SessionDep
import app.api.deps.microcontroller as deps

from app.models.microcontroller import (
    MicrocontrollerCreate,
    MicrocontrollerUpdate,
    MicrocontrollerPublic,
)
from app.models.message import Message

import app.service.microcontroller as service


router = APIRouter()


@router.get("/{id}", response_model=MicrocontrollerPublic, dependencies=[Depends(get_current_user)])
def read_microcontroller(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get microcontroller by ID.
    """

    microcontroller = service.get_microcontroller_by_id(session=session, microcontroller_id=id)

    if not microcontroller:
        raise HTTPException(status_code=404, detail="Microcontroller not found")
    
    return microcontroller


@router.post("/", response_model=MicrocontrollerPublic, dependencies=[Depends(deps.authorize_create_microcontroller)])
def create_microcontroller(
    *, session: SessionDep, microcontroller_in: MicrocontrollerCreate
) -> Any:
    """
    Create new microcontroller.
    """
    
    try:
        microcontroller = service.create_microcontroller(session=session, microcontroller_in=microcontroller_in)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return microcontroller


@router.put("/{id}", response_model=MicrocontrollerPublic, dependencies=[Depends(deps.authorize_update_microcontroller)])
def update_microcontroller(
    *,
    session: SessionDep,
    id: uuid.UUID,
    microcontroller_in: MicrocontrollerUpdate,
) -> Any:
    """
    Update a microcontroller.
    
    """
    try:
        updated_microcontroller = service.update_microcontroller(id=id, session=session, microcontroller_in=microcontroller_in)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not updated_microcontroller:
        raise HTTPException(status_code=404, detail="Microcontroller not found")
    
    return updated_microcontroller


@router.delete("/{id}", response_model=Message, dependencies=[Depends(deps.authorize_delete_microcontroller)])
def delete_microcontroller(
    *, session: SessionDep, id: uuid.UUID
) -> Message:
    """
    Delete a microcontroller.
    """
    
    deleted_microcontroller = service.delete_microcontroller(session=session, id=id)
    
    if not deleted_microcontroller:
        raise HTTPException(status_code=404, detail="Microcontroller not found")
    
    return Message(message="Microcontroller deleted successfully")
