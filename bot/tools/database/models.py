from sqlalchemy import MetaData, Table, String, Integer, Float, Column, Text
from sqlalchemy.orm import declarative_base
from . import engine

Base = declarative_base(engine)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(255), nullable=False)
    
Base.metadata.create_all()