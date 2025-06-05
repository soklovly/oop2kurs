from sqlalchemy.orm import Session
from datetime import datetime
from models import Todolist, Item

def create_todolist(db: Session, name: str):
    db_todolist = Todolist(name=name)
    db.add(db_todolist)
    db.commit()
    db.refresh(db_todolist)
    return db_todolist

def get_todolists(db: Session):
    return db.query(Todolist).filter(Todolist.deleted_at == None).all()

def get_todolist(db: Session, todolist_id: int):
    todolist = db.query(Todolist).filter(Todolist.id == todolist_id, Todolist.deleted_at == None).first()
    if todolist and todolist.total_items > 0:
        todolist.progress = (todolist.completed_items / todolist.total_items) * 100
    return todolist

def delete_todolist(db: Session, todolist_id: int):
    db_todolist = db.query(Todolist).filter(Todolist.id == todolist_id).first()
    if db_todolist:
        db_todolist.deleted_at = datetime.now()
        db.commit()
    return db_todolist


def create_item(db: Session, name: str, text: str, todolist_id: int):
    db_item = Item(name=name, text=text, todolist_id=todolist_id)
    db.add(db_item)
    
    todolist = db.query(Todolist).filter(Todolist.id == todolist_id).first()
    todolist.total_items += 1
    db.commit()
    
    return db_item

def get_items(db: Session, todolist_id: int):
    return db.query(Item).filter(Item.todolist_id == todolist_id, Item.deleted_at == None).all()

def update_item(db: Session, item_id: int, is_done: bool):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        old_status = db_item.is_done
        db_item.is_done = is_done
        
        todolist = db.query(Todolist).filter(Todolist.id == db_item.todolist_id).first()
        if old_status != is_done:
            todolist.completed_items += 1 if is_done else -1
        db.commit()
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db_item.deleted_at = datetime.now()
        
        todolist = db.query(Todolist).filter(Todolist.id == db_item.todolist_id).first()
        todolist.total_items -= 1
        if db_item.is_done:
            todolist.completed_items -= 1
        db.commit()
    return db_item