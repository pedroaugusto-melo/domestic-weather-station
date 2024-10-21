from sqlmodel import Session
import uuid

import app.crud.user as crud
from app.models.user import User, UserCreate, UserUpdate, UpdatePassword, UserRegister

from app.core.config import settings
from app.utils import generate_new_account_email, send_email
from app.core.security import verify_password


def get_user_by_id(session: Session, id: uuid.UUID) -> User | None:
    return crud.get_user_by_id(session=session, user_id=id)


def count_users(session: Session) -> int:
    return crud.count_users(session=session)


def get_users(session: Session, skip: int = 0, limit: int = 1000) -> list[User]:
    return crud.get_users(session=session, skip=skip, limit=limit)


def get_user_by_email(session: Session, email: str) -> User | None:
    return crud.get_user_by_email(session=session, email=email)


def create_user(session: Session, user_create: UserCreate) -> User:
    existing_user = get_user_by_email(session=session, email=user_create.email)

    if existing_user is not None:
        raise ValueError("User with this email already exists.")
    
    return crud.create_user(session=session, user_create=user_create)


def send_email_on_new_user(user: UserCreate) -> None:
    if settings.emails_enabled and user.email:
        email_data = generate_new_account_email(
            email_to=user.email, username=user.email, password=user.password
        )
        send_email(
            email_to=user.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )


def update_user(session: Session, id: uuid.UUID, user_in: UserUpdate) -> User | None:
    db_user = get_user_by_id(session=session, id=id)

    if db_user is None:
        return None

    if user_in.email:
        existing_user = get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != db_user.id:
            raise ValueError("User with this email already exists.")
    
    return crud.update_user(session=session, db_user=db_user, user_in=user_in)


def update_password_me(session: Session, db_user: User, password_info: UpdatePassword) -> User:
    if not verify_password(password_info.current_password, db_user.hashed_password):
        raise ValueError("Incorrect password")
    if password_info.current_password == password_info.new_password:
        raise ValueError("New password cannot be the same as the current one")
    
    user_in = UserUpdate(password=password_info.new_password)
    crud.update_user(session=session, db_user=db_user, user_in=user_in)


def delete_user(session: Session, id: uuid.UUID) -> User | None:
    user = get_user_by_id(session=session, id=id)

    if user is None:
        return None

    return crud.delete_user(session=session, user=user)


def register_user(session: Session, user_in: UserRegister) -> User:
    user_create = UserCreate.model_validate(user_in)
    return create_user(session=session, user_create=user_create)