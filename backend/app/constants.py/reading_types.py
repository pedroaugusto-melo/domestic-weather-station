from enum import StrEnum

class ReadingTypes(StrEnum):
    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    HEAT_INDEX = 'heat_index'
    GAS_LEVEL = 'gas_level'