from fastapi import APIRouter

from app.api.routes import (
    login, 
    users, 
    utils, 
    sensors, 
    microcontrollers,
    weather_station_models,
    weather_stations,
    weather_station_models_sensors,
    temperature_readings,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(sensors.router, prefix="/sensors", tags=["sensors"])
api_router.include_router(microcontrollers.router, prefix="/microcontrollers", tags=["microcontrollers"])
api_router.include_router(weather_station_models.router, prefix="/weather_station_models", tags=["weather_station_models"])
api_router.include_router(weather_stations.router, prefix="/weather_stations", tags=["weather_stations"])
api_router.include_router(weather_station_models_sensors.router, prefix="/weather_station_models_sensors", tags=["weather_station_models_sensors"])
api_router.include_router(temperature_readings.router, prefix="/temperature_readings", tags=["temperature_readings"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])