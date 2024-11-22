from fastapi import APIRouter

from app.api.routes import (
    data_readings,
    login, 
    users, 
    utils, 
    sensors, 
    microcontrollers,
    weather_station_models,
    weather_stations,
    weather_station_models_sensors,
    chat,
    analysis,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(sensors.router, prefix="/sensors", tags=["sensors"])
api_router.include_router(microcontrollers.router, prefix="/microcontrollers", tags=["microcontrollers"])
api_router.include_router(weather_station_models.router, prefix="/weather-station-models", tags=["weather_station_models"])
api_router.include_router(weather_stations.router, prefix="/weather-stations", tags=["weather_stations"])
api_router.include_router(weather_station_models_sensors.router, prefix="/weather-station-models-sensors", tags=["weather_station_models_sensors"])
api_router.include_router(data_readings.router, prefix="/data-readings", tags=["data_readings"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])