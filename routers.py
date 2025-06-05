from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services import TodolistService, ItemService
from schemas import TodolistResponse, ItemResponse
from models import Base
from databases import Database
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

router = APIRouter()

# Подключение к БД
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

@router.post("/todolists/", response_model=TodolistResponse)
def create_todolist(name: str, db: Session = Depends(get_db)):
    service = TodolistService(db)
    return service.create(name)

@router.get("/todolists/", response_model=list[TodolistResponse])
def get_todolists(db: Session = Depends(get_db)):
    service = TodolistService(db)
    return service.get_all()

@router.delete("/todolists/{todolist_id}")
def delete_todolist(todolist_id: int, db: Session = Depends(get_db)):
    service = TodolistService(db)
    return service.delete(todolist_id)

@router.post("/items/", response_model=ItemResponse)
def create_item(name: str, text: str, todolist_id: int, db: Session = Depends(get_db)):
    service = ItemService(db)
    return service.create(name, text, todolist_id)