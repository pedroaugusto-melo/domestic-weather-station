import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

import app.service.user as service
import app.api.deps.user as deps
from app.api.deps.db import SessionDep
from app.models.user import UserCreate, UserPublic, UserRegister, UsersPublic, UserUpdate, UpdatePassword
from app.models.message import Message


router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(deps.get_current_active_superuser)],
    response_model=UsersPublic,
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """

    count = service.count_users(session=session)
    users = service.get_users(session=session, skip=skip, limit=limit)

    return UsersPublic(data=users, count=count)


@router.post(
    "/", dependencies=[Depends(deps.get_current_active_superuser)], response_model=UserPublic
)
def create_user(*, session: SessionDep, user_in: UserCreate, background_tasks: BackgroundTasks) -> Any:
    """
    Create new user.
    """

    try:
        user = service.create_user(session=session, user_create=user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    background_tasks.add_task(service.send_email_on_new_user, user=user_in)

    return user


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *, session: SessionDep, user_in: UserUpdate, current_user: deps.CurrentUser
) -> Any:
    """
    Update own user.
    """
        
    updated_user = service.update_user(session=session, id=current_user.id, user_in=user_in)
    return updated_user


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *, session: SessionDep, body: UpdatePassword, current_user: deps.CurrentUser
) -> Any:
    """
    Update own password.
    """

    try:
        service.update_password_me(session=session, db_user=current_user, password_info=body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return Message(message="Password updated successfully")


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: deps.CurrentUser) -> Any:
    """
    Get current user.
    """

    return current_user


@router.delete("/me", response_model=Message)
def delete_user_me(session: SessionDep, current_user: deps.CurrentUser) -> Any:
    """
    Delete own user.
    """

    service.delete_user(session=session, id=current_user.id)
    return Message(message="User deleted successfully")


@router.post("/signup", response_model=UserPublic)
def register_user(session: SessionDep, user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """

    try:
        created_user = service.register_user(session=session, user_in=user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return created_user


@router.get("/{user_id}", response_model=UserPublic, dependencies=[Depends(deps.authorize_read_user)])
def read_user_by_id(
    user_id: uuid.UUID, session: SessionDep,
) -> Any:
    """
    Get a specific user by id.
    """
    
    user = service.get_user_by_id(session=session, user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(deps.get_current_active_superuser)],
    response_model=UserPublic,
)
def update_user(
    *,
    session: SessionDep,
    user_id: uuid.UUID,
    user_in: UserUpdate,
) -> Any:
    """
    Update a user.
    """

    try:
        updated_user = service.update_user(session=session, id=user_id, user_in=user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@router.delete("/{user_id}", dependencies=[Depends(deps.get_current_active_superuser)])
def delete_user(
    session: SessionDep, user_id: uuid.UUID
) -> Message:
    """
    Delete a user.
    """

    deleted_user = service.delete_user(session=session, id=user_id)

    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")

    return Message(message="User deleted successfully")
