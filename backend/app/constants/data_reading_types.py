from enum import StrEnum

from app.models.temperature_reading import TemperatureReading, TemperatureReadingCreate, TemperatureReadingUpdate, TemperatureReadingPublic
from app.models.gas_level_reading import GasLevelReading, GasLevelReadingCreate, GasLevelReadingUpdate, GasLevelReadingPublic
from app.models.humidity_reading import HumidityReading, HumidityReadingCreate, HumidityReadingUpdate, HumidityReadingPublic
from app.models.heat_index_reading import HeatIndexReading, HeatIndexReadingCreate, HeatIndexReadingUpdate, HeatIndexReadingPublic


class ReadingTypes(StrEnum):
    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    HEAT_INDEX = 'heat_index'
    GAS_LEVEL = 'gas_level'


ReadingClassesByType = {
    ReadingTypes.TEMPERATURE: TemperatureReading,
    ReadingTypes.GAS_LEVEL: GasLevelReading,
    ReadingTypes.HUMIDITY: HumidityReading,
}

DataReadingTypesClasses = TemperatureReading | GasLevelReading | HumidityReading | HeatIndexReading
DataReadingCreateTypesClasses = TemperatureReadingCreate | GasLevelReadingCreate | HumidityReadingCreate | HeatIndexReadingCreate
DataReadingUpdateTypesClasses = TemperatureReadingUpdate | GasLevelReadingUpdate | HumidityReadingUpdate | HeatIndexReadingUpdate
DataReadingPublicTypes = TemperatureReadingPublic | GasLevelReadingPublic | HumidityReadingPublic | HeatIndexReadingPublic