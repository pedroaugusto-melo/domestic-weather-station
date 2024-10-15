import uuid
from sqlmodel import SQLModel, Field, Relationship

# Shared properties
class MicrocontrollerBase(SQLModel):
    manufacturer: str
    component_reference: str
    datasheet_url: str
    description: str
    part_number: str = Field(unique=True, index=True)

# Properties to receive via API on creation
class MicrocontrollerCreate(MicrocontrollerBase):
    pass

# Properties to receive via API on update, all are optional
class MicrocontrollerUpdate(MicrocontrollerBase):
    manufacturer: str | None = None
    component_reference: str | None = None
    datasheet_url: str | None = None
    description: str | None = None
    part_number: str | None = None

# Database model
class Microcontroller(MicrocontrollerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    weather_station_models: list["WeatherStationModel"] = Relationship(back_populates="microcontroller") # type: ignore

# Properties to return via API
class MicrocontrollerPublic(MicrocontrollerBase):
    id: uuid.UUID

class MicrocontrollersPublic(SQLModel):
    data: list[MicrocontrollerPublic]
    count: int
