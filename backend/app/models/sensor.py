import uuid
from sqlmodel import SQLModel, Field, Column, ARRAY, String, Relationship

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
    manufacturer: str | None = None
    component_reference: str | None = None
    datasheet_url: str | None = None
    measuremnts_types: list[str] | None = None
    part_number: str | None = None


# Database model
class Sensor(SensorBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    measuremnts_types: list[str] = Field(sa_column=Column(ARRAY(String)))

    # Relationships
    weather_station_models: list["WeatherStationModelSensor"] = Relationship(back_populates="sensor", cascade_delete=True) # type: ignore
    temperature_readings: list["TemperatureReading"] = Relationship(back_populates="sensor", cascade_delete=True) # type: ignore
    gas_level_readings: list["GasLevelReading"] = Relationship(back_populates="sensor", cascade_delete=True) # type: ignore
    humidity_readings: list["HumidityReading"] = Relationship(back_populates="sensor", cascade_delete=True) # type: ignore
    heat_index_readings: list["HeatIndexReading"] = Relationship(back_populates="sensor", cascade_delete=True) # type: ignore

# Properties to return via API
class SensorPublic(SensorBase):
    id: uuid.UUID


class SensorsPublic(SQLModel):
    data: list[SensorPublic]
    count: int