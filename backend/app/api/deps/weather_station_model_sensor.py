from fastapi import HTTPException

from app.api.deps.user import CurrentUser


def authorize_read_weather_station_model_sensor(current_user: CurrentUser) -> None:
    pass


def authorize_create_weather_station_model_sensor(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions to create weather station model sensor")


def authorize_update_weather_station_model_sensor(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions to update weather station model sensor")


def authorize_delete_weather_station_model_sensor(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions to delete weather station model sensor")