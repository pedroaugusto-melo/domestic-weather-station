from fastapi import HTTPException
from app.api.deps.user import CurrentUser


def authorize_create_sensor(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    

def authorize_update_sensor(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
def authorize_delete_sensor(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")