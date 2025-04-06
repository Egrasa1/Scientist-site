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


