# utils.py
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])


def send_empresa_registration_email(email, link):
    """
    Envia l'enllaç de registre d'empresa amb token a l'email.
    """
    msg = Message(
        subject='Enllaç per registrar la teva empresa',
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )
    msg.body = f"""
Hola,

S'ha generat un enllaç únic per registrar la teva empresa.
Pots utilitzar-lo per crear la teva empresa al sistema:

{link}

Aquest enllaç caduca en 24 hores.

Salutacions,
L'equip de Consulmat
"""
    mail.send(msg)
