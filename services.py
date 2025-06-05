from sqlalchemy.orm import Session
from models import Todolist, Item
from datetime import datetime

class TodolistService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str):
        db_todolist = Todolist(name=name)
        self.db.add(db_todolist)
        self.db.commit()
        return db_todolist

    def get_all(self):
        return self.db.query(Todolist).filter(Todolist.deleted_at == None).all()

    def delete(self, todolist_id: int):
        todolist = self.db.query(Todolist).filter(Todolist.id == todolist_id).first()
        if todolist:
            todolist.deleted_at = datetime.now()
            self.db.commit()
        return todolist

class ItemService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, text: str, todolist_id: int):
        db_item = Item(name=name, text=text, todolist_id=todolist_id)
        self.db.add(db_item)
        self.db.commit()
        return db_item