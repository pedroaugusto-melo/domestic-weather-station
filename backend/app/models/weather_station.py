import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from app.models.user import User
from app.models.weather_station_model import WeatherStationModel

# Shared properties
class WeatherStationBase(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    weather_station_model_id: uuid.UUID = Field(foreign_key="weather_station_model.id")
    name: str
    part_number: str = Field(unique=True, index=True)
    description: Optional[str] = None

# Properties to receive via API on creation
class WeatherStationCreate(WeatherStationBase):
    pass

# Properties to receive via API on update, all are optional
class WeatherStationUpdate(SQLModel):
    user_id: Optional[uuid.UUID] = None
    weather_station_model_id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    part_number: Optional[str] = None
    description: Optional[str] = None

# Database model
class WeatherStation(WeatherStationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    # Relationships
    user: User = Relationship(back_populates="weather_stations")
    weather_station_model: WeatherStationModel = Relationship(back_populates="weather_stations")
    temperature_readings: list["TemperatureReading"] = Relationship(back_populates="weather_station", cascade_delete=True) # type: ignore
    gas_level_readings_readings: list["GasLevelReading"] = Relationship(back_populates="weather_station", cascade_delete=True) # type: ignore

    __tablename__ = "weather_station"

# Properties to return via API
class WeatherStationPublic(WeatherStationBase):
    id: uuid.UUID

class WeatherStationsPublic(SQLModel):
    data: List[WeatherStationPublic]
    count: int
