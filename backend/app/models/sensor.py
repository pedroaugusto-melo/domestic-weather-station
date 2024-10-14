import uuid
from sqlmodel import SQLModel, Field, Column, ARRAY, String

# Shared properties
class SensorBase(SQLModel):
    manufacturer: str
    component_reference: str
    datasheet_url: str
    measuremnts_types: list[str]
    part_number: str = Field(unique=True, index=True)

# Properties to receive via API on creation
class SensorCreate(SensorBase):
    pass


# Properties to receive via API on update, all are optional
class SensorUpdate(SensorBase):
    manufacturer: str | None
    component_reference: str | None
    datasheet_url: str | None
    measuremnts_types: list[str] | None
    part_number: str | None


# Database model
class Sensor(SensorBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    measuremnts_types: list[str] = Field(sa_column=Column(ARRAY(String)))


# Properties to return via API
class SensorPublic(SensorBase):
    id: uuid.UUID


class SensorsPublic(SQLModel):
    data: list[SensorPublic]
    count: int