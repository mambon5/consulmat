from flask import Flask, request, redirect, url_for, flash, render_template, jsonify, session
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime
import random
import pycountry
from zoneinfo import ZoneInfo

from app.models import db, User, Empresa, TimeRecord, PauseRecord, Incidencia, Comunidad, Pagador, Factura, Treballador, DataProcessingConsent, EventoLaboral, HorarioLaboral
from app.routes import auth, fichajes, privacidad, empresa, facturas, calendario
from app.services.email_service import configure_mail
from utils import get_serializer
import os
from pathlib import Path

# Obtener la ruta base del proyecto
BASE_DIR = Path(__file__).parent

app = Flask(__name__, template_folder=BASE_DIR / 'app' / 'templates')

# Configuración de la aplicación
import os
from dotenv import load_dotenv

load_dotenv()

# Construct database URL from environment variables
db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('DB_PASSWORD', '')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '3306')
db_name = os.getenv('DB_NAME', 'fichaje_db')

if db_password:
    database_url = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
else:
    database_url = f'mysql+pymysql://{db_user}@{db_host}:{db_port}/{db_name}'

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Inicialización de extensiones
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
mail = Mail(app)

# Configurar mail
configure_mail(app)

# Registro de blueprints
app.register_blueprint(auth.auth_bp)
app.register_blueprint(fichajes.fichajes_bp)
app.register_blueprint(privacidad.privacidad_bp)
app.register_blueprint(empresa.empresa_bp)
app.register_blueprint(facturas.facturas_bp)
app.register_blueprint(calendario.calendario_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def utility_processor():
    return {'now': datetime.now()}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
