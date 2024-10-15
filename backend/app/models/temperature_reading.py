import uuid
from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from app.models.sensor import Sensor 
from app.models.weather_station import WeatherStation


# Shared properties
class TemperatureReadingBase(SQLModel):
    sensor_id: uuid.UUID = Field(foreign_key="sensor.id")
    weather_station_id: uuid.UUID = Field(foreign_key="weather_station.id")
    value: float
    read_at: datetime

# Properties to receive via API on creation
class TemperatureReadingCreate(TemperatureReadingBase):
    pass

# Properties to receive via API on update, all are optional
class TemperatureReadingUpdate(SQLModel):
    sensor_id: Optional[uuid.UUID] = None
    weather_station_id: Optional[uuid.UUID] = None
    value: Optional[float] = None
    read_at: Optional[datetime] = None

# Database model
class TemperatureReading(TemperatureReadingBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    # Relationships
    sensor: Sensor = Relationship(back_populates="temperature_readings")
    weather_station: WeatherStation = Relationship(back_populates="temperature_readings")

    __tablename__ = "temperature_reading"

# Properties to return via API
class TemperatureReadingPublic(TemperatureReadingBase):
    id: uuid.UUID

class TemperatureReadingsPublic(SQLModel):
    data: List[TemperatureReadingPublic]
    count: int
