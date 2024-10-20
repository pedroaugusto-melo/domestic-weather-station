from fastapi import HTTPException
from app.api.deps.user import CurrentUser


def authorize_create_weather_station_model(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions to create weather station model")
    
def authorize_update_weather_station_model(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions to update weather station model")
    
def authorize_delete_weather_station_model(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions to delete weather station model")