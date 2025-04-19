import os
import smtplib
from email.mime.text import MIMEText
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Путь до папки в якой знаходиться нинешній файл

class BaseConfig:
    """Базована настройка"""
    
    APP_NAME = os.getenv("APP_NAME", "BIG BLACK PENCIL")
    SECRET_KEY = os.getenv("SECRET_KEY", "Опа, а що таке нема пароля? Плакі плакі")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    DEBUG_TB_ENABLED = False # Дебаг меню в браузері 
    WTF_CSRF_ENABLED = False # CSRF-защита (Cross-Site Request Forgery) 
    
    @staticmethod
    def configure(app):
        pass

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///" + os.path.join(BASE_DIR, "development.sqlite3")
    ) # Потрібно для того щоб підключатися до бази данних
    
class ProductionConfig(BaseConfig):
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///" + os.path.join(BASE_DIR, "production.sqlite3")
    )
    
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

def send_welcome_email(user_email):
    sender = "illya.d.donchenko@ukr.net"
    password = "T0XX2Udvx6MzPOOO"
    subject = "Вітаємо з реєстрацією!"
    body = "Вітаємо, ви зареєструвалися на нашому сайті з купою цікавих та захоплюючих новин. Сподіваємося ваш досвід користування нашим сайтом буде виключно позитивним"


    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = user_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, user_email, msg.as_string())
            print("Email sent to", user_email)
    except Exception as e:
        print("Email send failed:", e)




