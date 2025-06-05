from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Base, Todolist, Item
from schemas import TodolistCreate, TodolistResponse, ItemCreate, ItemResponse
from crud import (
    create_todolist, get_todolists, get_todolist, update_todolist, delete_todolist,
    create_item, get_items, get_item, update_item, delete_item
)
from databases import Database
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

app = FastAPI()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{
    os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

#Dependency для получения сессии базы данных
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@app.post("/todolists/", response_model=TodolistResponse)
def create_todolist_route(todolist: TodolistCreate, db: Session = Depends(get_db)):
    return create_todolist(db, todolist)

@app.get("/todolists/", response_model=list[TodolistResponse])
def read_todolists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_todolists(db, skip=skip, limit=limit)

@app.get("/todolists/{todolist_id}", response_model=TodolistResponse)
def read_todolist(todolist_id: int, db: Session = Depends(get_db)):
    todolist = get_todolist(db, todolist_id)
    if todolist is None:
        raise HTTPException(status_code=404, detail="Todolist not found")
    return todolist

@app.patch("/todolists/{todolist_id}", response_model=TodolistResponse)
def update_todolist_route(todolist_id: int, todolist: TodolistCreate, db: Session = Depends(get_db)):
    db_todolist = update_todolist(db, todolist_id, todolist)
    if db_todolist is None:
        raise HTTPException(status_code=404, detail="Todolist not found")
    return db_todolist

@app.delete("/todolists/{todolist_id}", response_model=TodolistResponse)
def delete_todolist_route(todolist_id: int, db: Session = Depends(get_db)):
    db_todolist = delete_todolist(db, todolist_id)
    if db_todolist is None:
        raise HTTPException(status_code=404, detail="Todolist not found")
    return db_todolist

#маршруты для Item
@app.post("/items/", response_model=ItemResponse)
def create_item_route(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)

@app.get("/items/", response_model=list[ItemResponse])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_items(db, skip=skip, limit=limit)

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.patch("/items/{item_id}", response_model=ItemResponse)
def update_item_route(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = update_item(db, item_id, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}", response_model=ItemResponse)
def delete_item_route(item_id: int, db: Session = Depends(get_db)):
    db_item = delete_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item