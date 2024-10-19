from sqlmodel import Session
import uuid

from app.models.microcontroller import Microcontroller, MicrocontrollerCreate, MicrocontrollerUpdate

import app.crud.microcontroller as crud


def get_microcontroller_by_id(*, session: Session, microcontroller_id: uuid.UUID) -> Microcontroller | None:
    return crud.get_microcontroller_by_id(session=session, microcontroller_id=microcontroller_id)


def create_microcontroller(*, session: Session, microcontroller_in: MicrocontrollerCreate) -> Microcontroller:
    return crud.create_microcontroller(session=session, microcontroller_in=microcontroller_in)


def update_microcontroller(*, session: Session, id: uuid.UUID, microcontroller_in: MicrocontrollerUpdate) -> Microcontroller:
    microcontroller = crud.get_microcontroller_by_id(session=session, microcontroller_id=id)

    if microcontroller is None:
        return None

    return crud.update_microcontroller(session=session, db_microcontroller=microcontroller, microcontroller_in=microcontroller_in)


def delete_microcontroller(*, session: Session, id: uuid.UUID) -> Microcontroller | None:
    microcontroller = crud.get_microcontroller_by_id(session=session, microcontroller_id=id)

    if microcontroller is None:
        return None

    return crud.delete_microcontroller(session=session, microcontroller=microcontroller)