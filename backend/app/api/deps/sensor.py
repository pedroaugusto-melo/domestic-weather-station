from fastapi import HTTPException
from app.api.deps.user import CurrentUser


def authorize_create_sensor(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions to create sensor")
    
def authorize_update_sensor(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions to update sensor")
    
def authorize_delete_sensor(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions to delete sensor")