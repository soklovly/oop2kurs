from sqlalchemy.orm import Session
from models import Todolist, Item

def create_todolist(db: Session, todolist):
    db_todolist = Todolist(**todolist.dict())
    db.add(db_todolist)
    db.commit()
    db.refresh(db_todolist)
    return db_todolist

def get_todolists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Todolist).offset(skip).limit(limit).all()

def get_todolist(db: Session, todolist_id: int):
    return db.query(Todolist).filter(Todolist.id == todolist_id).first()

def update_todolist(db: Session, todolist_id: int, todolist):
    db_todolist = db.query(Todolist).filter(Todolist.id == todolist_id).first()
    if db_todolist:
        for key, value in todolist.dict().items():
            setattr(db_todolist, key, value)
        db.commit()
        db.refresh(db_todolist)
    return db_todolist

def delete_todolist(db: Session, todolist_id: int):
    db_todolist = db.query(Todolist).filter(Todolist.id == todolist_id).first()
    if db_todolist:
        db.delete(db_todolist)
        db.commit()
    return db_todolist

def create_item(db: Session, item):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def update_item(db: Session, item_id: int, item):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item