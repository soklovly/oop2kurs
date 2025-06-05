from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Todolist(Base):
    __tablename__ = 'todolists'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    items = relationship("Item", back_populates="todolist")

class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    text = Column(String)
    is_done = Column(Boolean, default=False)
    todolist_id = Column(Integer, ForeignKey('todolists.id'))
    
    todolist = relationship("Todolist", back_populates="items")