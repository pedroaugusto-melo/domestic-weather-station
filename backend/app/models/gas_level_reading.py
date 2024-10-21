import uuid
from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from app.models.sensor import Sensor 
from app.models.weather_station import WeatherStation


# Shared properties
class GasLevelReadingBase(SQLModel):
    sensor_id: uuid.UUID = Field(foreign_key="sensor.id")
    weather_station_id: uuid.UUID = Field(foreign_key="weather_station.id")
    value: int
    read_at: datetime

# Properties to receive via API on creation
class GasLevelReadingCreate(GasLevelReadingBase):
    pass

# Properties to receive via API on update, all are optional
class GasLevelReadingUpdate(SQLModel):
    sensor_id: Optional[uuid.UUID] = None
    weather_station_id: Optional[uuid.UUID] = None
    value: Optional[int] = None
    read_at: Optional[datetime] = None

# Database model
class GasLevelReading(GasLevelReadingBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    # Relationships
    sensor: Sensor = Relationship(back_populates="gas_level_readings")
    weather_station: WeatherStation = Relationship(back_populates="gas_level_readings")

    __tablename__ = "gas_level_reading"

# Properties to return via API
class GasLevelReadingPublic(GasLevelReadingBase):
    id: uuid.UUID

class GasLevelReadingsPublic(SQLModel):
    data: List[GasLevelReadingPublic]
    count: int
