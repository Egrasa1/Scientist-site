from sqlalchemy import Column, Integer, ForeignKey
from .base import Base
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship



class Likes(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')
    date = Column(DateTime, default=datetime.utcnow)
