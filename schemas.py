from pydantic import BaseModel

class TodolistCreate(BaseModel):
    name: str

class TodolistResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True

class ItemCreate(BaseModel):
    name: str
    text: str
    is_done: bool = False
    todolist_id: int

class ItemResponse(BaseModel):
    id: int
    name: str
    text: str
    is_done: bool
    todolist_id: int
    
    class Config:
        orm_mode = True