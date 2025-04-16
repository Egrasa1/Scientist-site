import os
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from werkzeug.exceptions import HTTPException # Для опрацювання HTTP-помилок включно статус-коди 4xx та 5xx

login_manager = LoginManager()
db = SQLAlchemy(session_options={"autoflush": False}) 
# autoflush відповідая за автоматичной відправки змін в бд, 
# але це не комміт, перед виконанням любих запросів в цьой сесій

def create_app(environment="development"):
    from config import config
    from .routes import user_bp, post_bp
    from .models import User, AnonymousUser
    
    app = Flask(__name__)
    
    env = os.getenv("FLASK_ENV", environment) # берем статус проекта з .flaskenv або environment
    app.config.from_object(config[env]) # загружаемо всі конфігурацій з config описанний в файлі config.py
    config[env].configure(app)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
    
    # @login_manager.user_loader
    # def get_user(id):
    #     return User.query.get(int(id))
    
    login_manager.login_view = 'auth_signin'
    login_manager.login_message_category = 'info'
    login_manager.anonymous_user = AnonymousUser
    
    @app.errorhandler(HTTPException)
    def handler_http_error(exc):
        return render_template('error.html', error=exc), exc.code
    
    return app