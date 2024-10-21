import uuid
from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from app.models.sensor import Sensor 
from app.models.weather_station import WeatherStation


# Shared properties
class HeatIndexReadingBase(SQLModel):
    sensor_id: uuid.UUID = Field(foreign_key="sensor.id")
    weather_station_id: uuid.UUID = Field(foreign_key="weather_station.id")
    value: float
    read_at: datetime

# Properties to receive via API on creation
class HeatIndexReadingCreate(HeatIndexReadingBase):
    pass

# Properties to receive via API on update, all are optional
class HeatIndexReadingUpdate(SQLModel):
    sensor_id: Optional[uuid.UUID] = None
    weather_station_id: Optional[uuid.UUID] = None
    value: Optional[float] = None
    read_at: Optional[datetime] = None

# Database model
class HeatIndexReading(HeatIndexReadingBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    # Relationships
    sensor: Sensor = Relationship(back_populates="heat_index_readings")
    weather_station: WeatherStation = Relationship(back_populates="heat_index_readings")

    __tablename__ = "heat_index_reading"

# Properties to return via API
class HeatIndexReadingPublic(HeatIndexReadingBase):
    id: uuid.UUID

class HeatIndexReadingsPublic(SQLModel):
    data: List[HeatIndexReadingPublic]
    count: int
