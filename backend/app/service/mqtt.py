import paho.mqtt.client as mqtt
from enum import StrEnum
from sqlmodel import Session
import json

from app.core.config import settings
from app.core.db import engine
from app.constants.reading_types import ReadingTypes

import app.service.sensor as sensor_service
import app.service.weather_station as weather_station_service
import app.service.data_reading as data_reading_service

from app.models.temperature_reading import TemperatureReadingCreate
from app.models.gas_level_reading import GasLevelReadingCreate
from app.models.humidity_reading import HumidityReadingCreate

class MQTTTopics(StrEnum):
    TEMPERATURE = "temperature/domestic_weather_station"
    HUMIDITY = "humidity/domestic_weather_station"
    HEAT_INDEX = "heat_index/domestic_weather_station"
    GAS_LEVEL = "gas_level/domestic_weather_station"


def on_mqtt_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())

    with Session(engine) as session:
        sensor_part_number = data['sensor_part_number']
        sensor = sensor_service.get_sensor_by_part_number(session=session, part_number=sensor_part_number)
        
        if sensor is None:
            raise ValueError(f"Sensor with part number {sensor_part_number} not found")

        weather_station_part_number = data['station_part_number']
        weather_station = weather_station_service.get_weather_station_by_part_number(session=session, part_number=weather_station_part_number)

        if weather_station is None:
            raise ValueError(f"Weather Station with part number {weather_station_part_number} not found")

        if msg.topic == MQTTTopics.TEMPERATURE:
            temperature_reading = TemperatureReadingCreate(
                sensor_id=sensor.id,
                weather_station_id=weather_station.id,
                value=data['temperature'],
                read_at=data['read_at']
            )
            data_reading_service.create_data_reading(session=session, data_reading_in=temperature_reading, reading_type=ReadingTypes.TEMPERATURE)
        elif msg.topic == MQTTTopics.GAS_LEVEL:
            gas_level_reading = GasLevelReadingCreate(
                sensor_id=sensor.id,
                weather_station_id=weather_station.id,
                value=data['gas_level'],
                read_at=data['read_at']
            )
            data_reading_service.create_data_reading(session=session, data_reading_in=gas_level_reading, reading_type=ReadingTypes.GAS_LEVEL)
        elif msg.topic == MQTTTopics.HUMIDITY:
            humidity_reading = HumidityReadingCreate(
                sensor_id=sensor.id,
                weather_station_id=weather_station.id,
                value=data['humidity'],
                read_at=data['read_at']
            )
            data_reading_service.create_data_reading(session=session, data_reading_in=humidity_reading, reading_type=ReadingTypes.HUMIDITY)

def setup_mqtt_client():
    client = mqtt.Client()
    client.username_pw_set(settings.MQTT_BROKER_USERNAME, settings.MQTT_BROKER_PASSWORD)
    client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, 60)
    
    client.on_message = on_mqtt_message
    
    client.subscribe(MQTTTopics.TEMPERATURE)
    client.subscribe(MQTTTopics.HUMIDITY)
    client.subscribe(MQTTTopics.HEAT_INDEX)
    client.subscribe(MQTTTopics.GAS_LEVEL)
    
    client.loop_start()

