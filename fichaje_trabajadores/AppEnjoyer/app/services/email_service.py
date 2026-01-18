from flask_mail import Message
from app import mail
from flask import current_app


# Configuración Flask-Mail; remitent des del qual s'envia el mail de confirmació al crear un compte
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True # TLS sistema de seguretat per xifrar la info quan envies correu de verificacio que s'usa de forma standard : Transport Layer Security
app.config['MAIL_USE_SSL'] = False  # SSL desactivat - sistema de seguretat antic : Secure Sockets Layer
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

# per tema enviar email confirmacio al crear compte
def send_verification_email(email, code):
    msg = Message('Código de verificación', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f'Tu código de verificación es: {code}'
    mail.send(msg)
    

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
