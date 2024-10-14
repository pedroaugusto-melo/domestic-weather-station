import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends

from app.api.deps import CurrentUser, SessionDep, get_current_user

from app.models.microcontroller import (
    MicrocontrollerCreate,
    MicrocontrollerUpdate,
    MicrocontrollerPublic,
)
from app.models.message import Message

import app.crud.microcontroller as crud


router = APIRouter()


@router.get("/{id}", response_model=MicrocontrollerPublic, dependencies=[Depends(get_current_user)])
def read_microcontroller(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get microcontroller by ID.
    """

    microcontroller = crud.get_microcontroller_by_id(session=session, microcontroller_id=id)

    if not microcontroller:
        raise HTTPException(status_code=404, detail="Microcontroller not found")
    
    return microcontroller


@router.post("/", response_model=MicrocontrollerPublic)
def create_microcontroller(
    *, session: SessionDep, current_user: CurrentUser, microcontroller_in: MicrocontrollerCreate
) -> Any:
    """
    Create new microcontroller.
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    microcontroller = crud.create_microcontroller(session=session, microcontroller_in=microcontroller_in)
    return microcontroller


@router.put("/{id}", response_model=MicrocontrollerPublic)
def update_microcontroller(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    microcontroller_in: MicrocontrollerUpdate,
) -> Any:
    """
    Update a microcontroller.
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    microcontroller = crud.get_microcontroller_by_id(session=session, microcontroller_id=id)
    
    if not microcontroller:
        raise HTTPException(status_code=404, detail="Microcontroller not found")
    
    updated_microcontroller = crud.update_microcontroller(
        session=session,
        db_microcontroller=microcontroller,
        microcontroller_in=microcontroller_in,
    )
    return updated_microcontroller


@router.delete("/{id}")
def delete_microcontroller(
    *, session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a microcontroller.
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    microcontroller = crud.get_microcontroller_by_id(session=session, microcontroller_id=id)
    
    if not microcontroller:
        raise HTTPException(status_code=404, detail="Microcontroller not found")
    
    crud.delete_microcontroller(session=session, microcontroller=microcontroller)
    return Message(message="Microcontroller deleted successfully")
