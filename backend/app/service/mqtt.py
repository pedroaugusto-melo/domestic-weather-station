import paho.mqtt.client as mqtt
from enum import StrEnum
from sqlmodel import Session
import json

from app.core.config import settings
from app.core.db import engine

import app.crud.sensor as sensor_crud
import app.crud.weather_station as weather_station_crud

import app.crud.temperature_reading as temperature_reading_crud
from app.models.temperature_reading import TemperatureReadingCreate

class MQTTTopics(StrEnum):
    TEMPERATURE = "temperature/domestic_weather_station"
    HUMIDITY = "humidity/domestic_weather_station"
    HEAT_INDEX = "heat_index/domestic_weather_station"
    GAS_LEVEL = "gas_level/domestic_weather_station"


def on_mqtt_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())

    if msg.topic == MQTTTopics.TEMPERATURE:
        with Session(engine) as session:
            sensor_part_number = data['sensor_part_number']
            sensor = sensor_crud.get_sensor_by_part_number(session=session, part_number=sensor_part_number)
            
            weather_station_part_number = data['station_part_number']
            weather_station = weather_station_crud.get_weather_station_by_part_number(session=session, part_number=weather_station_part_number)

            temperature_reading = TemperatureReadingCreate(
                sensor_id=sensor.id,
                weather_station_id=weather_station.id,
                value=data['temperature'],
                read_at=data['read_at']
            )
            temperature_reading_crud.create_temperature_reading(session=session, temperature_reading_in=temperature_reading)
        
    

    pass

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
