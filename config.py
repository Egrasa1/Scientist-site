import os

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
    
    


# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# sender_email = os.getenv('SENDER_EMAIL') 
# sender_password = os.getenv('SENDER_PASSWORD')

# def send_mail():
#         subject = "Вітаємо з реєстрацією!"
#         body = 'Вітаємо, ви зареєструвалися на нашому сайті з купою цікавих та захоплюючих новин. Сподіваємося ваш досвід користування нашим сайтом буде виключно позитивним'

#         msg = MIMEMultipart()
#         msg['From'] = sender_email
#         msg['To'] = receiver_email
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))
#         try:
#             with smtplib.SMTP_SSL("smtp.ukr.net", 465) as server:
#                 server.login(sender_email, sender_password)
#                 server.sendmail(sender_email, receiver_email, msg.as_string())
#         except smtplib.SMTPException:
#             print("Error: unable to mail")