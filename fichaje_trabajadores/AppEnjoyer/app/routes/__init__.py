from .auth import auth_bp
from .fichajes import fichajes_bp
from .privacidad import privacidad_bp
from .calendario import calendario_bp
from .empresa import empresa_bp
from .facturas import facturas_bp
from .admin_views import admin_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(fichajes_bp)
    app.register_blueprint(privacidad_bp)
    app.register_blueprint(calendario_bp)
    app.register_blueprint(empresa_bp)
    app.register_blueprint(facturas_bp)
    app.register_blueprint(admin_bp)
