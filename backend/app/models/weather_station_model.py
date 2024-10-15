import uuid
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

from app.models.microcontroller import Microcontroller


# Shared properties
class WeatherStationModelBase(SQLModel):
    microcontroller_id: uuid.UUID = Field(foreign_key="microcontroller.id")
    name: str
    description: str
    release_date: date

# Properties to receive via API on creation
class WeatherStationModelCreate(WeatherStationModelBase):
    pass

# Properties to receive via API on update, all are optional
class WeatherStationModelUpdate(SQLModel):
    microcontroller_id: uuid.UUID | None = None
    name: str | None = None
    description: str | None = None
    release_date: date | None = None

# Database model
class WeatherStationModel(WeatherStationModelBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Relationships
    microcontroller: Microcontroller = Relationship(back_populates="weather_station_models")
    weather_stations: list["WeatherStation"] = Relationship(back_populates="weather_station_model") # type: ignore

    __tablename__ = "weather_station_model"

# Properties to return via API
class WeatherStationModelPublic(WeatherStationModelBase):
    id: uuid.UUID

class WeatherStationModelsPublic(SQLModel):
    data: list[WeatherStationModelPublic]
    count: int
