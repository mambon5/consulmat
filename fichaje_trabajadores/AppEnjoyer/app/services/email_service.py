import os
from flask_mail import Message
from app import mail
from flask import current_app
from dotenv import load_dotenv

load_dotenv()

def configure_mail(app):
    """Configurar Flask-Mail amb variables d'entorn"""
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@example.com')
    return app

def send_verification_email(email, code):
    msg = Message('Código de verificación',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[email])
    msg.body = f'Tu código de verificación es: {code}'
    mail.send(msg)


def send_empresa_registration_email(email, link):
    msg = Message(
        subject='Enllaç per registrar la teva empresa',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[email]
    )
    msg.body = f"""
Hola,

S'ha generat un enllaç únic per registrar la teva empresa:

{link}

Caduca en 24 hores.
"""
    mail.send(msg)
