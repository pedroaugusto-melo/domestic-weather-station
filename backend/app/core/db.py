from sqlmodel import Session, create_engine

from app.core.config import settings

from app.models.user import UserCreate
from app.models.microcontroller import MicrocontrollerCreate
from app.models.sensor import SensorCreate
from app.models.weather_station_model import WeatherStationModelCreate
from app.models.weather_station_model_sensor import WeatherStationModelSensorCreate
from app.models.weather_station import WeatherStationCreate

import app.crud.user as crud_user
import app.crud.microcontroller as crud_microcontroller
import app.crud.sensor as crud_sensor
import app.crud.weather_station_model as crud_weather_station_model
import app.crud.weather_station_model_sensor as crud_weather_station_model_sensor
import app.crud.weather_station as crud_weather_station


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def init_db(session: Session) -> None:
    # create the first superuser
    user_in = UserCreate(
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
        full_name="DWS Admin"
    )
    user = crud_user.create_user(session=session, user_create=user_in)
    
    # create microcontroller
    microcontroller_in = MicrocontrollerCreate(
        manufacturer="Espressif",
        component_reference="ESP32",
        datasheet_url="https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32_datasheet_en.pdf",
        description="Controlador ESP32 com WiFi e Bluetooth embarcado",
        part_number="1",
    )
    microcontroller = crud_microcontroller.create_microcontroller(session=session, microcontroller_in=microcontroller_in)

    # create sensors
    dht22_in = SensorCreate(
        manufacturer="Aosong Electronics",
        component_reference="DHT22",
        datasheet_url="https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf",
        part_number="1",
        measuremnts_types=["temperature", "humidity"],
    )
    mq135_in = SensorCreate(
        manufacturer="Winsen",
        component_reference="MQ135",
        datasheet_url="https://www.winsen-sensor.com/d/files/PDF/Semiconductor%20Gas%20Sensor/MQ135%20(Ver1.4)%20-%20Manual.pdf",
        part_number="2",
        measuremnts_types=["gas_level"],
    )
    dht22 = crud_sensor.create_sensor(session=session, sensor_in=dht22_in)
    mq135 = crud_sensor.create_sensor(session=session, sensor_in=mq135_in)

    # create weather station model
    weather_station_model_in = WeatherStationModelCreate(
        microcontroller_id=microcontroller.id,
        name="Estação Meteorológica v1",
        description="Estação meteorológica com ESP32, DHT22 e MQ135",
        release_date="2024-10-09",
    )
    weather_station_model = crud_weather_station_model.create_weather_station_model(session=session, weather_station_model_in=weather_station_model_in)

    # create weather station model sensors
    weather_station_model_sensor_dht22 = WeatherStationModelSensorCreate(
        weather_station_model_id=weather_station_model.id,
        sensor_id=dht22.id,
    )
    weather_station_model_sensor_mq135 = WeatherStationModelSensorCreate(
        weather_station_model_id=weather_station_model.id,
        sensor_id=mq135.id,
    )
    crud_weather_station_model_sensor.create_weather_station_model_sensor(session=session, wsms_in=weather_station_model_sensor_dht22)
    crud_weather_station_model_sensor.create_weather_station_model_sensor(session=session, wsms_in=weather_station_model_sensor_mq135)

    # create weather station
    weather_station_in = WeatherStationCreate(
        user_id=user.id,
        weather_station_model_id=weather_station_model.id,
        part_number="1",
        name="Estação Meteorológica 1",
        description="Primeira estação meteorológica do projeto",
    )
    crud_weather_station.create_weather_station(session=session, weather_station_in=weather_station_in)