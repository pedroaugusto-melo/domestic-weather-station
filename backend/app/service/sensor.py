from sqlmodel import Session
import uuid

from app.models.sensor import Sensor, SensorCreate, SensorUpdate

import app.crud.sensor as crud


def get_sensor_by_id(*, session: Session, sensor_id: uuid.UUID) -> Sensor | None:
    return crud.get_sensor_by_id(session=session, sensor_id=sensor_id)


def create_sensor(*, session: Session, sensor_in: SensorCreate) -> Sensor:
    return crud.create_sensor(session=session, sensor_in=sensor_in)


def get_sensor_by_part_number(*, session: Session, part_number: str) -> Sensor | None:
    return crud.get_sensor_by_part_number(session=session, part_number=part_number)


def update_sensor(*, session: Session, id: uuid.UUID, sensor_in: SensorUpdate) -> Sensor | None:
    sensor = get_sensor_by_id(session=session, sensor_id=id)

    if sensor is None:
        return None

    return crud.update_sensor(session=session, db_sensor=sensor, sensor_in=sensor_in)


def delete_sensor(*, session: Session, id: uuid.UUID) -> Sensor | None:
    sensor = get_sensor_by_id(session=session, sensor_id=id)

    if sensor is None:
        return None

    return crud.delete_sensor(session=session, sensor=sensor)