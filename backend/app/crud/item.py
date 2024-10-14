import uuid

from sqlmodel import Session, select, func
from app.models.item import Item, ItemCreate, ItemUpdate


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def update_item(*, session: Session, db_item: Item, item_in: ItemUpdate) -> Item:
    item_data = item_in.model_dump(exclude_unset=True)
    db_item.sqlmodel_update(item_data)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def get_item_by_id(*, session: Session, item_id: uuid.UUID) -> Item | None:
    return session.get(Item, item_id)


def count_items(*, session: Session, owner_id: uuid.UUID) -> int:
    statement = select(func.count()).select_from(Item).where(Item.owner_id == owner_id)
    return session.exec(statement).one()


def get_items(*, session: Session, owner_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[Item]:
    statement = select(Item).where(Item.owner_id == owner_id).offset(skip).limit(limit)
    return session.exec(statement).all()


def delete_item(*, session: Session, item: Item) -> Item:
    session.delete(item)
    session.commit()
    return item
