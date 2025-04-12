from sqlalchemy import Column, String, Integer, Enum
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SqlEnum
from enum import Enum

class RoleEnum(Enum):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    passwords = Column(String(60), nullable=False)
    email = Column(String(250), unique=True)
    role = Column(SqlEnum(RoleEnum, name="role_enum"), default=RoleEnum.USER, nullable=False)

posts = relationship('Post', back_populates='author')
likes = relationship('Likes', back_populates='user')