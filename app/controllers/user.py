from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from app.models.base import Base, session
from app.models.users import User

class UserController:
    @staticmethod
    def create_user(db: session, name: str, password: str, email: str) -> User:
        new_user = User(
            name=name,
            passwords=password,
            email=email
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def get_user_by_id(db: session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_all_users(db: session) -> list[User]:
        return db.query(User).all()

    @staticmethod
    def update_user_name(db: session, user_id: int, new_name: str) -> User:
        user = UserController.get_user_by_id(db, user_id)
        if user:
            user.name = new_name
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def update_user_email(db: session, user_id: int, new_email: str) -> User:
        user = UserController.get_user_by_id(db, user_id)
        if user:
            user.email = new_email
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def update_user_password(db: session, user_id: int, new_password: str) -> User:
        user = UserController.get_user_by_id(db, user_id)
        if user:
            user.passwords = new_password
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: session, user_id: int) -> bool:
        user = UserController.get_user_by_id(db, user_id)
        if user:
            db.delete(user)
            db.commit()
            return True
        return False