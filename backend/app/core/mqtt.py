import paho.mqtt.client as mqtt
from enum import StrEnum
import json

from app.core.config import settings

class MQTTTopics(StrEnum):
    TEMPERATURE = "temperature/domestic_weather_station"
    HUMIDITY = "humidity/domestic_weather_station"
    HEAT_INDEX = "heat_index/domestic_weather_station"
    GAS_LEVEL = "gas_level/domestic_weather_station"


def on_mqtt_message(client, userdata, msg):
    # print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")
    
    # data = json.loads(msg.payload.decode())

    # if msg.topic == MQTTTopics.TEMPERATURE:
    #     print(f"Temperatura recebida: {data['temperature']}")
    # elif msg.topic == MQTTTopics.HUMIDITY:
    #     print(f"Umidade recebida: {data['humidity']}")
    # elif msg.topic == MQTTTopics.HEAT_INDEX:
    #     print(f"Índice de calor recebido: {data['heat_index']}")
    # elif msg.topic == MQTTTopics.GAS_LEVEL:
    #     print(f"Nível de gás recebido: {data['gas_level']}")
    
    # print("\n")
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

