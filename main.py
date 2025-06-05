from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Base, Todolist, Item
from schemas import TodolistResponse, ItemResponse
from crud import (
    create_todolist, get_todolists, get_todolist, delete_todolist,
    create_item, get_items, update_item, delete_item
)
from databases import Database
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

app = FastAPI()
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@app.post("/todolists/", response_model=TodolistResponse)
def create_todolist_route(name: str, db: Session = Depends(get_db)):
    return create_todolist(db, name)

@app.get("/todolists/", response_model=list[TodolistResponse])
def read_todolists(db: Session = Depends(get_db)):
    return get_todolists(db)

@app.get("/todolists/{todolist_id}", response_model=TodolistResponse)
def read_todolist(todolist_id: int, db: Session = Depends(get_db)):
    todolist = get_todolist(db, todolist_id)
    if not todolist:
        raise HTTPException(status_code=404, detail="Todolist not found")
    return todolist

@app.delete("/todolists/{todolist_id}", response_model=TodolistResponse)
def delete_todolist_route(todolist_id: int, db: Session = Depends(get_db)):
    todolist = delete_todolist(db, todolist_id)
    if not todolist:
        raise HTTPException(status_code=404, detail="Todolist not found")
    return todolist

@app.post("/items/", response_model=ItemResponse)
def create_item_route(name: str, text: str, todolist_id: int, db: Session = Depends(get_db)):
    return create_item(db, name, text, todolist_id)

@app.get("/items/{todolist_id}", response_model=list[ItemResponse])
def read_items(todolist_id: int, db: Session = Depends(get_db)):
    return get_items(db, todolist_id)

@app.patch("/items/{item_id}", response_model=ItemResponse)
def update_item_route(item_id: int, is_done: bool, db: Session = Depends(get_db)):
    item = update_item(db, item_id, is_done)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/items/{item_id}", response_model=ItemResponse)
def delete_item_route(item_id: int, db: Session = Depends(get_db)):
    item = delete_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item