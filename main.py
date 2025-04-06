from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase



engine = create_engine('sqlite:///test.db',echo=True)
#Session = sessionmaker(bind=engine)



class Base(DeclarativeBase):
    pass


def create_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


from sqlalchemy import Column, String, Integer, ForeignKey

from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship



create_db()
class Likes(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')
    date = Column(DateTime, default=datetime.utcnow)



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    passwords = Column(String(60), nullable=False)
    email = Column(String(250), unique=True)

posts = relationship('Post', back_populates='author')
likes = relationship('Likes', back_populates='user')



class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='likes')
    tittle = Column(String(100), nullable=False)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow)