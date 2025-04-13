from flask import Flask
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv



load_dotenv()

sender_email = os.getenv('SENDER_EMAIL') 
sender_password = os.getenv('SENDER_PASSWORD')










def send_mail():
        subject = "Вітаємо з реєстрацією!"
        body = 'Вітаємо, ви зареєструвалися на нашому сайті з купою цікавих та захоплюючих новин. Сподіваємося ваш досвід користування нашим сайтом буде виключно позитивним'

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        try:
            with smtplib.SMTP_SSL("smtp.ukr.net", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
        except smtplib.SMTPException:
            print("Error: unable to mail")