from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from app.models import create_db, drop_db

import os


app = Flask(__name__, template_folder='app/templates')
app.secret_key= os.getenv('SECRET_KEY')

create_db()


from app.routes import *



if __name__ == '__main__':
    app.run(debug=True)