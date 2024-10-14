import uuid
from sqlmodel import Session, select

from app.models.microcontroller import (
    Microcontroller,
    MicrocontrollerCreate,
    MicrocontrollerUpdate,
)


def create_microcontroller(
    *, session: Session, microcontroller_in: MicrocontrollerCreate
) -> Microcontroller:
    db_obj = Microcontroller.model_validate(microcontroller_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_microcontroller(
    *, session: Session, db_microcontroller: Microcontroller, microcontroller_in: MicrocontrollerUpdate
) -> Microcontroller:
    microcontroller_data = microcontroller_in.model_dump(exclude_unset=True)
    db_microcontroller.sqlmodel_update(microcontroller_data)
    session.add(db_microcontroller)
    session.commit()
    session.refresh(db_microcontroller)
    return db_microcontroller


def get_microcontroller_by_id(
    *, session: Session, microcontroller_id: uuid.UUID
) -> Microcontroller | None:
    return session.get(Microcontroller, microcontroller_id)


def get_microcontroller_by_part_number(
    *, session: Session, part_number: str
) -> Microcontroller | None:
    statement = select(Microcontroller).where(Microcontroller.part_number == part_number)
    return session.exec(statement).first()


def delete_microcontroller(
    *, session: Session, microcontroller: Microcontroller
) -> Microcontroller:
    session.delete(microcontroller)
    session.commit()
    return microcontroller