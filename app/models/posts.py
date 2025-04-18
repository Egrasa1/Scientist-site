from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime

# from .base import Base
from app import db
from .utils import ModelMixin

class Post(db.Model, ModelMixin):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tittle = Column(String(100), nullable=False)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    
    author = relationship('User', back_populates='likes')