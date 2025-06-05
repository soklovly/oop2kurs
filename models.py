from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Todolist(Base):
    __tablename__ = 'todolists'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    deleted_at = Column(DateTime, nullable=True)  
    completed_items = Column(Integer, default=0) 
    total_items = Column(Integer, default=0)      

class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    text = Column(String)
    is_done = Column(Boolean, default=False)
    todolist_id = Column(Integer, ForeignKey('todolists.id'))
    deleted_at = Column(DateTime, nullable=True)  