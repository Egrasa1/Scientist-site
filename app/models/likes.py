from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime

# from .base import Base
from app import db
from .utils import ModelMixin


class Likes(db.Model, ModelMixin):
    __tablename__ = 'likes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    date = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')
