from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from app.models.base import Base, session
from app.models.users import User

#Create
def create_user(name: str, password: str, email: str) -> User:
    new_user = User(
        name=name,
        passwords=password,  
        email=email
    )
    session.add(new_user)
    session.commit()
    return new_user

#READ
# Get user by ID
def get_user_by_id(user_id: int) -> User:
    return session.query(User).filter(User.id == user_id).first()

# Get user by email
def get_user_by_email(email: str) -> User:
    return session.query(User).filter(User.email == email).first()

#get all from db
def get_all_users() -> list[User]:
    return session.query(User).all()

# UPDATE
def update_user_name(user_id: int, new_name: str) -> User:
    user = get_user_by_id(user_id)
    if user:
        user.name = new_name
        session.commit()
    return user

def update_user_email(user_id: int, new_email: str) -> User:
    user = get_user_by_id(user_id)
    if user:
        user.email = new_email
        session.commit()
    return user

def update_user_password(user_id: int, new_password: str) -> User:

    user = get_user_by_id(user_id)
    if user:
        user.passwords = new_password  
        session.commit()
    return user

# DELETE
def delete_user(user_id: int) -> bool:
    user = get_user_by_id(user_id)
    if user:
        session.delete(user)
        session.commit()
        return True
    return False