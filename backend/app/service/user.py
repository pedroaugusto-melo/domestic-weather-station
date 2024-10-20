from sqlmodel import Session
import uuid

import app.crud.user as crud_user
from app.models.user import User


def get_user_by_id(session: Session, id: uuid.UUID) -> User | None:
    return crud_user.get_user_by_id(session=session, user_id=id)