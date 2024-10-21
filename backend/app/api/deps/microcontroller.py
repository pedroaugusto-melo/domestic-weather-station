from fastapi import HTTPException
from app.api.deps.user import CurrentUser


def authorize_create_microcontroller(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions to create microcontroller")
    
def authorize_update_microcontroller(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions to update microcontroller")
    
def authorize_delete_microcontroller(current_user: CurrentUser) -> None:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions to delete microcontroller")