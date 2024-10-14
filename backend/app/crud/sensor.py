import uuid
from sqlmodel import Session, select

from app.models.sensor import Sensor, SensorCreate, SensorUpdate


def create_sensor(*, session: Session, sensor_in: SensorCreate) -> Sensor:
    db_obj = Sensor.model_validate(sensor_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_sensor(*, session: Session, db_sensor: Sensor, sensor_in: SensorUpdate) -> Sensor:
    sensor_data = sensor_in.model_dump(exclude_unset=True)
    db_sensor.sqlmodel_update(sensor_data)
    session.add(db_sensor)
    session.commit()
    session.refresh(db_sensor)
    return db_sensor


def get_sensor_by_id(*, session: Session, sensor_id: uuid.UUID) -> Sensor | None:
    return session.get(Sensor, sensor_id)


def get_sensor_by_part_number(*, session: Session, part_number: str) -> Sensor | None:
    statement = select(Sensor).where(Sensor.part_number == part_number)
    session_sensor = session.exec(statement).first()
    return session_sensor


def delete_sensor(*, session: Session, sensor: Sensor) -> Sensor:
    session.delete(sensor)
    session.commit()
    return sensor