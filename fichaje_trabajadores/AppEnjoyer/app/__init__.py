from flask import Flask, request, session
from flask_login import LoginManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
bcrypt = Bcrypt()
babel = Babel()

def get_locale():
    # 1. Comprova si hi ha una aplicació activa i si som dins un context de petició (request)
    # Això evita errors quan s'executen comandes de terminal o s'inicialitza l'app
    from flask import has_request_context
    if not has_request_context():
        return 'es'
        
    # 2. Si l'usuari ha triat un idioma manualment (desat a la sessió), el fem servir
    if 'language' in session:
        return session['language']
        
    # 3. Si no ha triat res, detecta l'idioma del seu navegador d'entre els teus 3 (ca, es, en)
    # Si el navegador no té cap d'aquests, escollirà 'es' per defecte
    return request.accept_languages.best_match(['ca', 'es', 'en']) or 'es'

def create_app():
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    app.jinja_env.globals['now'] = datetime.now()
    app.jinja_env.globals['get_locale'] = get_locale

    # Database configuration
    if os.environ.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    else:
        DB_USER = os.environ.get('DB_USER', 'root')
        DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
        DB_HOST = os.environ.get('DB_HOST', 'localhost')
        DB_PORT = os.environ.get('DB_PORT', '3306')
        DB_NAME = os.environ.get('DB_NAME', 'fichaje_db')
        if DB_PASSWORD:
            app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Mail configuration
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@example.com')

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    login_manager.login_view = 'auth.login'

    from .routes import register_blueprints
    register_blueprints(app)

    return app
