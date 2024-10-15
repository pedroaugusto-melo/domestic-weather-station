import uuid
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint

from app.models.weather_station_model import WeatherStationModel
from app.models.sensor import Sensor

# Shared properties
class WeatherStationModelSensorBase(SQLModel):
    weather_station_model_id: uuid.UUID = Field(foreign_key="weather_station_model.id")
    sensor_id: uuid.UUID = Field(foreign_key="sensor.id")

# Properties to receive via API on creation
class WeatherStationModelSensorCreate(WeatherStationModelSensorBase):
    pass

# Properties to receive via API on update
class WeatherStationModelSensorUpdate(SQLModel):
    weather_station_model_id: Optional[uuid.UUID] = None
    sensor_id: Optional[uuid.UUID] = None

# Database model
class WeatherStationModelSensor(WeatherStationModelSensorBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Relationships
    weather_station_model: WeatherStationModel = Relationship(
        back_populates="sensors"
    )
    sensor: Sensor = Relationship(
        back_populates="weather_station_models"
    )

    __tablename__ = "weather_station_model_sensor"
    __table_args__ = (
        UniqueConstraint("weather_station_model_id", "sensor_id"),
    )

# Properties to return via API
class WeatherStationModelSensorPublic(WeatherStationModelSensorBase):
    id: uuid.UUID