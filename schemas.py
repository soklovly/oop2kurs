from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TodolistResponse(BaseModel):
    id: int
    name: str
    progress: float = Field(0.0, ge=0, le=100)  
    deleted_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class ItemResponse(BaseModel):
    id: int
    name: str
    text: str
    is_done: bool
    todolist_id: int
    deleted_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True