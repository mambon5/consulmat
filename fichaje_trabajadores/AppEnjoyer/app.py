from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dotenv import load_dotenv #env per no tenir les contrasenyes visibles
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
import locale
import random
import pycountry # per obtenir una llista amb tots els paísos del món

# packages importants er descarregar factures
from flask import send_file, redirect, url_for, flash
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

mail = Mail(app)

# per tema enviar email confirmacio al crear compte
def send_verification_email(email, code):
    msg = Message('Código de verificación', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f'Tu código de verificación es: {code}'
    mail.send(msg)
    
# Configuración de la base de datos
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

# Configuración Flask-Mail; remitent des del qual s'envia el mail de confirmació al crear un compte
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

@app.route('/register', methods=['GET', 'POST'])
def register():
    email_sent = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        # Si el usuario está intentando verificar el email
        if 'email_code' in request.form:
            user = User.query.filter_by(username=username, email=email).first()
            if user and request.form['email_code'] == user.email_code:
                user.email_verified = True
                db.session.commit()
                flash('Email verificado y cuenta creada correctamente.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Código de verificación incorrecto.', 'danger')
                email_sent = True
                return render_template('register.html', email_sent=email_sent, username=username, name=name, email=email, phone=phone)

        # Validación: usuario único
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.', 'danger')
            return render_template('register.html')

        # Generar código de verificación
        email_code = str(random.randint(100000, 999999))

        # Guardar usuario temporalmente (no verificado)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(
            username=username,
            password=hashed_password,
            name=name,
            email=email,
            phone=phone,
            email_code=email_code,  # Usamos el mismo campo para el código
            data_consent=False,
            consent_date=None,
            data_retention_days=1460
        )
        db.session.add(user)
        db.session.commit()

        # Enviar email
        send_verification_email(email, email_code)
        email_sent = True
        flash('Se ha enviado un email de verificación a tu correo.', 'info')
        return render_template('register.html', email_sent=email_sent, username=username, name=name, email=email, phone=phone)
    return render_template('register.html')

# Configuración de locale
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')
    except locale.Error:
        # Si no se puede configurar el locale español, usamos el predeterminado
        locale.setlocale(locale.LC_TIME, '')


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email_code = db.Column(db.String(6), nullable=True)
    email_verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), nullable=False, default='employee')
    data_consent = db.Column(db.Boolean, nullable=False, default=False)
    consent_date = db.Column(db.DateTime, nullable=True)
    data_retention_days = db.Column(db.Integer, nullable=False, default=365)
    records = db.relationship('TimeRecord', backref='user', lazy=True)
    treballador = db.relationship('Treballador', backref='user', uselist=False)

class Comunidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    cif = db.Column(db.String(20), nullable=False, unique=True)
    ciudad = db.Column(db.String(100), nullable=False)
    codi_postal = db.Column(db.Integer, nullable=True)
    provincia = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    id_pagador = db.Column(db.Integer, db.ForeignKey('pagadors.id_pagador'), nullable=True)  
    fecha_alta = db.Column(db.Date, nullable=False)
    latitud = db.Column(db.Numeric(9,6), nullable=False)
    longitud = db.Column(db.Numeric(9,6), nullable=False)

class Factura(db.Model):
    __tablename__ = 'factures'

    id_factura = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_comunitat = db.Column(db.Integer, db.ForeignKey('comunidad.id'), nullable=False)

    tipus_feina = db.Column(db.String(255), nullable=False)  # e.g. "Limpieza mensual..."
    document_de_pago = db.Column(db.String(255), nullable=False)  # e.g. "pago a cuenta..."
    regimen_impuestos = db.Column(db.String(255), nullable=True)  # pot ser nullable si no sempre s’omple

    comunitat = db.relationship('Comunidad', backref='factures', lazy=True)

class LineaFactura(db.Model): # LineaFactura es para ve los detalles legales obligatorios de una factura
    __tablename__ = 'linea_factura'
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('factures.id_factura'), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

class Treballador(db.Model):
    __tablename__ = 'treballadors'

    id_treballador = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuari = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    departament = db.Column(
        db.Enum('parkings', 'comunitats', 'oficines', name='departament_enum'),
        nullable=False
    )
    adreca = db.Column(db.String(255), nullable=True)
    ciutat = db.Column(db.String(100), nullable=True)
    codi_postal = db.Column(db.Integer, nullable=True)

    sexe = db.Column(
        db.Enum('f', 'm', 'no', name='sexe_enum'),
        nullable=True
    )
    nacionalitat = db.Column(db.String(100), nullable=True)
    edat = db.Column(db.Integer, nullable=True)

    carnet_conduir = db.Column(
        db.Enum('si', 'no', name='carnet_conduir_enum'),
        nullable=True
    )
    vehicle_propi = db.Column(
        db.Enum('si', 'no', name='vehicle_propi_enum'),
        nullable=True
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Calendari(db.Model):
    __tablename__ = 'calendari'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    treballador_id = db.Column(db.Integer, db.ForeignKey('treballadors.id_treballador'), nullable=False)
    dia_setmana = db.Column(db.Enum('Dll','Dm','Dx','Dj','Dv','Ds','Dg', name='dia_setmana_enum'), nullable=False)
    comunitat_id = db.Column(db.Integer, db.ForeignKey('comunidad.id'), nullable=False)
    hora_inici = db.Column(db.Time, nullable=False)
    hora_fi = db.Column(db.Time, nullable=False)

    treballador = db.relationship('Treballador', backref=db.backref('calendari', lazy=True))
    comunitat = db.relationship('Comunidad', backref=db.backref('calendari', lazy=True))

    def __repr__(self):
        return f'<Calendari {self.treballador_id} {self.dia_setmana} {self.comunitat_id} {self.hora_inici}-{self.hora_fi}>'



class Pagador(db.Model):
    __tablename__ = 'pagadors'

    id_pagador = db.Column(db.Integer, primary_key=True)
    nom_pagador = db.Column(db.String(255), nullable=False)
    telefon = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(255), nullable=True, unique=True)
    direccio = db.Column(db.String(255), nullable=True)
    ciutat = db.Column(db.String(100), nullable=True)
    codi_postal = db.Column(db.Integer, nullable=True)  # Transformat a numèric

    # (Opcional) Relació amb comunitats si vols establir una connexió:
    comunitats = db.relationship('Comunidad', backref='pagador', lazy=True)


class TimeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime, nullable=True)
    check_in_latitude = db.Column(db.Float, nullable=True)
    check_in_longitude = db.Column(db.Float, nullable=True)
    check_in_accuracy = db.Column(db.Float, nullable=True)
    check_out_latitude = db.Column(db.Float, nullable=True)
    check_out_longitude = db.Column(db.Float, nullable=True)
    check_out_accuracy = db.Column(db.Float, nullable=True)

     # 🔽 afegim propietats
    @property
    def total_pause_seconds(self):
        return sum(
            (p.pause_end - p.pause_start).total_seconds()
            for p in self.pauses if p.pause_end
        )

    @property
    def total_pause_hms(self):
        total = int(self.total_pause_seconds or 0)
        hours = total // 3600
        minutes = (total % 3600) // 60
        seconds = total % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"


class PauseRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_record_id = db.Column(db.Integer, db.ForeignKey('time_record.id'), nullable=False)
    pause_start = db.Column(db.DateTime, nullable=False)
    pause_end = db.Column(db.DateTime, nullable=True)
    pause_date = db.Column(db.Date, nullable=False)  # Nou camp per associar la pausa a un dia
    # Opcional: geolocalització de la pausa
    pause_latitude = db.Column(db.Float, nullable=True)
    pause_longitude = db.Column(db.Float, nullable=True)
    pause_accuracy = db.Column(db.Float, nullable=True)
    time_record = db.relationship('TimeRecord', backref=db.backref('pauses', lazy=True))

class DataProcessingConsent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    consent_type = db.Column(db.String(50), nullable=False)
    granted = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(ZoneInfo("Europe/Madrid")))    
    ip_address = db.Column(db.String(45), nullable=True)

# calendari laboral: horaris, festius, dies de treball

class HorarioLaboral(db.Model):
    __tablename__ = 'horarios_laborales'
    id = db.Column(db.Integer, primary_key=True)
    id_treballador = db.Column(db.Integer, db.ForeignKey('treballadors.id_treballador'), nullable=False)
    id_comunitat = db.Column(db.Integer, db.ForeignKey('comunidad.id'), nullable=False)
    dia_semana = db.Column(db.Integer, nullable=False)  # 0=Lunes, 6=Domingo
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)

    treballador = db.relationship('Treballador', backref='horarios_laborales')
    comunitat = db.relationship('Comunidad', backref='horarios_laborales')

class EventoLaboral(db.Model):
    __tablename__ = 'eventos_laborales'
    id = db.Column(db.Integer, primary_key=True)
    id_treballador = db.Column(db.Integer, db.ForeignKey('treballadors.id_treballador'), nullable=False)
    id_comunitat = db.Column(db.Integer, db.ForeignKey('comunidad.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=True)  # Puede ser None si es festivo
    hora_fin = db.Column(db.Time, nullable=True)
    tipo_evento = db.Column(db.Enum('trabajo', 'festivo_nacional', 'festivo_autonomico', 'festivo_local', name='tipo_evento_enum'), nullable=False, default='trabajo')

    treballador = db.relationship('Treballador', backref='eventos_laborales')
    comunitat = db.relationship('Comunidad', backref='eventos_laborales')
class Incidencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_record_id = db.Column(db.Integer, db.ForeignKey('time_record.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=lambda: datetime.now(ZoneInfo("Europe/Madrid")).date())
    time = db.Column(db.Time, nullable=False, default=lambda: datetime.now(ZoneInfo("Europe/Madrid")).time())
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user = db.relationship('User', backref=db.backref('incidencies', lazy=True))
    time_record = db.relationship('TimeRecord', backref=db.backref('incidencies', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def generate_pdf_report(records, user, report_type):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=20
    )
    
    # Add company header
    elements.append(Paragraph("INFORME DE REGISTRO HORARIO", title_style))
    
    # Add report information
    period_text = {
        'week': 'Última Semana',
        'month': 'Último Mes',
        'year': 'Último Año'
    }
    
    elements.append(Paragraph(f"Empleado: {user.name}", header_style))
    elements.append(Paragraph(f"Periodo: {period_text[report_type]}", header_style))
    elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d de %B de %Y')}", header_style))
    elements.append(Spacer(1, 20))
    
    # Prepare table data
    data = [['Fecha', 'Entrada', 'Salida', 'Horas Trabajadas']]
    total_hours = timedelta()
    
    for record in records:
        check_in_date = record.check_in.strftime('%d/%m/%Y')
        check_in_time = record.check_in.strftime('%H:%M')
        
        if record.check_out:
            check_out_time = record.check_out.strftime('%H:%M')
            duration = record.check_out - record.check_in
            hours_worked = f"{duration.seconds//3600}:{(duration.seconds//60)%60:02d}"
            total_hours += duration
        else:
            check_out_time = '-'
            hours_worked = '-'
            
        data.append([check_in_date, check_in_time, check_out_time, hours_worked])
    
    # Create table
    table = Table(data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # Add summary
    if total_hours.total_seconds() > 0:
        total_hours_str = f"{int(total_hours.total_seconds()//3600)}:{int((total_hours.total_seconds()//60)%60):02d}"
        elements.append(Paragraph(f"Total de horas trabajadas: {total_hours_str}", header_style))
    
    # Add footer
    elements.append(Spacer(1, 40))
    footer_text = """Este informe ha sido generado automáticamente por el sistema de control horario.
    Los datos mostrados están sujetos a la política de privacidad y protección de datos de la empresa."""
    elements.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

@app.route('/generate_report', methods=['GET', 'POST'])
@login_required
def generate_report():
    if request.method == 'POST':
        report_type = request.form.get('report_type', 'week')
        
        # Calculate date range
        end_date = datetime.now()
        if report_type == 'week':
            start_date = end_date - timedelta(days=7)
        elif report_type == 'month':
            start_date = end_date - timedelta(days=30)
        else:  # year
            start_date = end_date - timedelta(days=365)
        
        # Get records
        records = TimeRecord.query.filter(
            TimeRecord.user_id == current_user.id,
            TimeRecord.check_in >= start_date,
            TimeRecord.check_in <= end_date
        ).order_by(TimeRecord.check_in.desc()).all()
        
        # Generate PDF
        pdf_buffer = generate_pdf_report(records, current_user, report_type)
        
        # Send file
        return send_file(
            pdf_buffer,
            download_name=f'registro_horario_{datetime.now().strftime("%Y%m%d")}.pdf',
            mimetype='application/pdf'
        )
    
    return render_template('report.html')

@app.route('/')
@login_required
def index():
    records = TimeRecord.query.filter_by(user_id=current_user.id).order_by(TimeRecord.check_in.desc()).all()
    active_record = TimeRecord.query.filter_by(user_id=current_user.id, check_out=None).first()
    today = datetime.now(ZoneInfo("Europe/Madrid")).date()
    today_incidencies = Incidencia.query.filter_by(user_id=current_user.id, date=today).order_by(Incidencia.time.desc()).all()
    return render_template('index.html', records=records, active_record=active_record, today_incidencies=today_incidencies)

@app.route('/check_in', methods=['POST'])
@login_required
def check_in():
    active_record = TimeRecord.query.filter_by(user_id=current_user.id, check_out=None).first()
    if active_record:
        flash('Ya tienes un registro activo', 'warning')
    else:
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        accuracy = request.form.get('accuracy')
        record = TimeRecord(
            user_id=current_user.id,
            check_in=datetime.now(),
            check_in_latitude=float(latitude) if latitude else None,
            check_in_longitude=float(longitude) if longitude else None,
            check_in_accuracy=float(accuracy) if accuracy else None
        )
        db.session.add(record)
        db.session.commit()
        flash('Registro de entrada exitoso', 'success')
    return redirect(url_for('index'))

@app.route('/check_out', methods=['POST'])
@login_required
def check_out():
    active_record = TimeRecord.query.filter_by(user_id=current_user.id, check_out=None).first()
    if active_record:
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        accuracy = request.form.get('accuracy')
        active_record.check_out = datetime.now()
        active_record.check_out_latitude = float(latitude) if latitude else None
        active_record.check_out_longitude = float(longitude) if longitude else None
        active_record.check_out_accuracy = float(accuracy) if accuracy else None
        db.session.commit()
        flash('Registro de salida exitoso', 'success')
    else:
        flash('No tienes un registro activo', 'warning')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Por favor, introduce usuario y contraseña.', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash(f'Bienvenido/a, {user.name}', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.before_request
def require_data_consent():
    # Solo para usuarios autenticados y rutas privadas
    if current_user.is_authenticated:
        # Excluye rutas públicas y la propia ruta de consentimiento
        allowed_routes = ['data_consent', 'logout', 'privacy_policy', 'aviso_legal', 'static']
        if not current_user.data_consent and request.endpoint not in allowed_routes:
            return redirect(url_for('data_consent'))

@app.route('/data-consent', methods=['GET', 'POST'])
@login_required
def data_consent():
    if request.method == 'POST':
        consent_type = request.form.get('consent_type')
        granted = request.form.get('granted') == 'true'
        
        consent = DataProcessingConsent(
            user_id=current_user.id,
            consent_type=consent_type,
            granted=granted,
            ip_address=request.remote_addr
        )
        
        if consent_type == 'general':
            current_user.data_consent = granted
            current_user.consent_date = datetime.utcnow() if granted else None
            
        db.session.add(consent)
        db.session.commit()
        
        flash('Preferencias de privacidad actualizadas', 'success')
        return redirect(url_for('privacy_settings'))
        
    return render_template('data_consent.html')

@app.route('/privacy-settings')
@login_required
def privacy_settings():
    return render_template('privacy_settings.html')

@app.route('/aviso-legal')
def aviso_legal():
    return render_template('aviso_legal.html')

@app.route('/export-data')
@login_required
def export_data():
    # Get user data
    user_data = {
        'username': current_user.username,
        'name': current_user.name,
        'email': current_user.email,
        'records': []
    }
    
    # Get time records
    records = TimeRecord.query.filter_by(user_id=current_user.id).all()
    for record in records:
        user_data['records'].append({
            'check_in': record.check_in.isoformat(),
            'check_out': record.check_out.isoformat() if record.check_out else None
        })
    
    # Create JSON response
    return jsonify(user_data)

@app.route('/delete-data', methods=['POST'])
@login_required
def delete_data():
    if request.form.get('confirm') == 'true':
        # Delete time records
        TimeRecord.query.filter_by(user_id=current_user.id).delete()
        # Delete consent records
        DataProcessingConsent.query.filter_by(user_id=current_user.id).delete()
        # Delete user
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
        flash('Tu cuenta y todos tus datos han sido eliminados', 'success')
        return redirect(url_for('login'))
    
    flash('Confirmación requerida para eliminar datos', 'error')
    return redirect(url_for('privacy_settings'))

@app.route('/calendario-laboral')
@login_required
def calendario_laboral():
    #eventos = []
    eventos = [
    {"title": "Trabajo", "start": "2025-09-03T09:00:00", "end": "2025-09-03T17:00:00", "color": "#1976d2"},
    {"title": "Festivo Nacional", "start": "2025-10-12", "allDay": True, "color": "#e53935"},
]
    treballador_id = request.args.get('treballador_id', type=int)

    # Si es admin y selecciona trabajador, muestra ese calendario
    if current_user.role == 'admin':
        # Si no se selecciona, muestra el primero
        if not treballador_id:
            treballador = Treballador.query.first()
        else:
            treballador = Treballador.query.get(treballador_id)
        # Para el desplegable de selección
        treballadors = Treballador.query.all()
    else:
        # Si es trabajador, solo el suyo
        treballador = current_user.treballador
        treballadors = None

    if treballador:
        eventos_db = EventoLaboral.query.filter_by(id_treballador=treballador.id_treballador).all()
        horarios_db = HorarioLaboral.query.filter_by(id_treballador=treballador.id_treballador).all()
    else:
        eventos_db = []
        horarios_db = []

    # Eventos puntuales (festivos y días especiales)
    for evento in eventos_db:
        eventos.append({
            "title": evento.tipo_evento.replace('_', ' ').capitalize(),
            "start": evento.fecha.isoformat(),
            "allDay": True if not evento.hora_inicio else False,
            "color": "#e53935" if "festivo" in evento.tipo_evento else "#1976d2"
        })

    # Horarios recurrentes (Lunes a Viernes, etc.)
    from calendar import monthrange
    from datetime import date

    today = date.today()
    year = today.year
    month = today.month
    num_days = monthrange(year, month)[1]

    for horario in horarios_db:
        for day in range(1, num_days + 1):
            d = date(year, month, day)
            if d.weekday() == horario.dia_semana:
                eventos.append({
                    "title": "Trabajo",
                    "start": datetime.combine(d, horario.hora_inicio).isoformat(),
                    "end": datetime.combine(d, horario.hora_fin).isoformat(),
                    "color": "#1976d2"
                })

    return render_template('calendari.html', eventos=eventos, treballadors=treballadors, treballador_seleccionat=treballador)

@app.route('/create_admin', methods=['GET', 'POST'])
@login_required
def create_admin():
    # Verificar si el usuario actual es admin
    if not current_user.role == 'admin':
        flash('No tienes permisos para crear administradores.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        email = request.form.get('email')
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.', 'danger')
            return redirect(url_for('create_admin'))
        
        # Crear nuevo usuario admin
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_admin = User(
            username=username,
            password=hashed_password,
            name=name,
            email=email,
            role='admin',
            data_consent=True,
            consent_date=datetime.utcnow(),
            data_retention_days=365
        )
        
        db.session.add(new_admin)
        try:
            db.session.commit()
            flash('Administrador creado exitosamente.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear el administrador.', 'danger')
            return redirect(url_for('create_admin'))
    
    return render_template('create_admin.html')

@app.route('/create_empleat', methods=['GET', 'POST'])
@login_required
def create_empleat():
    # Verificar si el usuario actual es admin
    if not current_user.role == 'admin':
        flash('No tienes permisos para crear empleados.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        email = request.form.get('email')
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.', 'danger')
            return redirect(url_for('create_empleat'))
        
        # Crear nuevo usuario admin
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_admin = User(
            username=username,
            password=hashed_password,
            name=name,
            email=email,
            role='employee',
            data_consent=True,
            consent_date=datetime.utcnow(),
            data_retention_days=365
        )
        
        db.session.add(new_admin)
        try:
            db.session.commit()
            flash('Empleado creado exitosamente.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear el empleado.', 'danger')
            return redirect(url_for('create_empleat'))
    
    return render_template('create_empleat.html')

@app.route('/create_treballador', methods=['GET', 'POST'])
@login_required
def create_treballador():
    # Solo los administradores pueden crear trabajadores
    if current_user.role != 'admin':
        flash('No tienes permisos para crear trabajadores.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Datos del usuario
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        email = request.form.get('email')

        # Verificar que el usuario no exista
        if User.query.filter_by(username=username).first():
            flash('Ya existe un usuario con ese nombre.', 'danger')
            return redirect(url_for('create_treballador'))

        # Crear usuario
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        nuevo_usuario = User(
            username=username,
            password=hashed_password,
            name=name,
            email=email,
            role='employee',
            data_consent=True,
            consent_date=datetime.utcnow(),
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        # Datos del trabajador
        departament = request.form.get('departament')
        adreca = request.form.get('adreca')
        ciutat = request.form.get('ciutat')
        codi_postal = request.form.get('codi_postal')
        sexe = request.form.get('sexe')
        nacionalitat = request.form.get('nacionalitat')
        edat = request.form.get('edat')
        carnet_conduir = request.form.get('carnet_conduir')
        vehicle_propi = request.form.get('vehicle_propi')

        nou_treballador = Treballador(
            id_usuari=nuevo_usuario.id,
            departament=departament,
            adreca=adreca,
            ciutat=ciutat,
            codi_postal=int(codi_postal) if codi_postal else None,
            sexe=sexe,
            nacionalitat=nacionalitat,
            edat=int(edat) if edat else None,
            carnet_conduir=carnet_conduir,
            vehicle_propi=vehicle_propi,
            created_at=datetime.utcnow()
        )

        db.session.add(nou_treballador)
        db.session.commit()

        flash('Trabajador creado exitosamente.', 'success')
        return redirect(url_for('index'))
    
    # Obtenir tots els països
    paisos = [{'code': country.alpha_2, 'name': country.name} for country in pycountry.countries]

    return render_template('create_treballador.html', paisos = paisos)


@app.route('/create_comunitat', methods=['GET', 'POST'])
@login_required
def create_comunitat():
    if current_user.role != 'admin':
        flash('No tienes permisos para crear comunidades.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cif = request.form.get('cif')
        ciudad = request.form.get('ciudad')
        provincia = request.form.get('provincia')
        codi_postal = request.form.get('codi_postal')
        direccion = request.form.get('direccion')
        fecha_alta = request.form.get('fecha_alta')
        latitud = request.form.get('latitud')
        longitud = request.form.get('longitud')

        if Comunidad.query.filter_by(cif=cif).first():
            flash('Ya existe una comunidad con ese CIF.', 'danger')
            return redirect(url_for('create_comunitat'))

        nueva_comunidad = Comunidad(
            nombre=nombre,
            cif=cif,
            ciudad=ciudad,
            provincia=provincia,
            direccion=direccion,
            codi_postal=codi_postal,
            latitud=latitud,
            longitud=longitud,
            fecha_alta=fecha_alta
        )

        try:
            db.session.add(nueva_comunidad)
            db.session.commit()
            flash('Comunidad creada exitosamente.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la comunidad: {str(e)}', 'danger')
            return redirect(url_for('create_comunitat'))

    # Si no és POST, renderitzem el formulari
    return render_template('create_comunitat.html')


@app.route('/create_pagador', methods=['GET', 'POST'])
@login_required
def create_pagador():
    if current_user.role != 'admin':
        flash('No tens permisos per crear pagadors.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        nom_pagador = request.form.get('nom_pagador')
        telefon = request.form.get('telefon')
        email = request.form.get('email')
        direccio = request.form.get('direccio')
        ciutat = request.form.get('ciutat')
        codi_postal = request.form.get('codi_postal')

        if Pagador.query.filter_by(email=email).first():
            flash('Ja existeix un pagador amb aquest correu.', 'danger')
            return redirect(url_for('create_pagador'))

        nou_pagador = Pagador(
            nom_pagador=nom_pagador,
            telefon=telefon,
            email=email,
            direccio=direccio,
            ciutat=ciutat,
            codi_postal=codi_postal
        )

        try:
            db.session.add(nou_pagador)
            db.session.commit()
            flash('Pagador creat correctament.', 'success')
            return redirect(url_for('llistar_pagadors'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el pagador: {str(e)}', 'danger')
            return redirect(url_for('create_pagador'))

    return render_template('create_pagador.html')

@app.route('/pagadors')
@login_required
def llistar_pagadors():
    if current_user.role != 'admin':
        flash('No tens permisos per veure aquesta pàgina.', 'danger')
        return redirect(url_for('index'))

    pagadors = Pagador.query.order_by(Pagador.nom_pagador.asc()).all()
    return render_template('llistat_pagadors.html', pagadors=pagadors)

@app.route('/usuaris')
@login_required
def llistar_usuaris():
    if current_user.role != 'admin':
        flash('No tens permisos per accedir a aquesta pàgina.', 'danger')
        return redirect(url_for('index'))

    usuaris = User.query.order_by(User.name.asc()).all()
    return render_template('llistat_usuaris.html', usuaris=usuaris)

@app.route('/treballadors')
def llistar_treballadors():
    treballadors = Treballador.query.all()
    return render_template("llistat_treballadors.html", treballadors=treballadors)

@app.route('/usuari/<int:user_id>')
@login_required
def perfil_usuari(user_id):
    user = User.query.get_or_404(user_id)
    treballador = user.treballador if user.role == 'employee' else None
    return render_template('perfil_usuari.html', user=user, treballador=treballador)

@app.route('/comunitats')
@login_required
def llistar_comunitats():
    if current_user.role != 'admin':
        flash('No tens permisos per accedir a aquesta pàgina.', 'danger')
        return redirect(url_for('index'))

    comunitats = Comunidad.query.order_by(Comunidad.fecha_alta.asc()).all()
    return render_template('llistat_comunitats.html', comunitats=comunitats)


# Ruta para listar facturas
@app.route('/factures')
@login_required
def llistar_factures():
    if current_user.role != 'admin':
        flash('No tens permisos per accedir a aquesta pàgina.', 'danger')
        return redirect(url_for('index'))

    factures = Factura.query.order_by(Factura.id_factura.desc()).all()
    return render_template('llistat_factures.html', factures=factures)

# Ruta per descarregar una factura concreta
@app.route('/factura/<int:factura_id>/download')
@login_required
def download_factura(factura_id):
    if current_user.role != 'admin':
        flash('No tens permisos per descarregar factures.', 'danger')
        return redirect(url_for('llistar_factures'))

    factura = Factura.query.get_or_404(factura_id)
    import io
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    y = 800
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, y, f"Factura ID: {factura.id_factura}")

    p.setFont("Helvetica", 12)
    y -= 30
    p.drawString(100, y, f"Comunitat: {factura.comunitat.nombre}")
    y -= 20
    p.drawString(100, y, f"Tipus de feina: {factura.tipus_feina}")
    y -= 20
    p.drawString(100, y, f"Document de pagament: {factura.document_de_pago}")
    y -= 20
    p.drawString(100, y, f"Règim d’impostos: {factura.regimen_impuestos or '-'}")
    # Afegeix més camps si cal

    p.showPage()
    p.save()
    buffer.seek(0)

    from flask import send_file
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'factura_{factura.id_factura}.pdf',
        mimetype='application/pdf'
    )

# Ruta per crear una factura nova
@app.route('/create_factura', methods=['GET', 'POST'])
@login_required
def create_factura():
    if not current_user.role == 'admin':
        flash('No tienes permisos para crear facturas.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        id_comunitat = request.form.get('id_comunitat')
        tipus_feina = request.form.get('tipus_feina')
        document_de_pago = request.form.get('document_de_pago')
        regimen_impuestos = request.form.get('regimen_impostos') or None

        nova_factura = Factura(
            id_comunitat=id_comunitat,
            tipus_feina=tipus_feina,
            document_de_pago=document_de_pago,
            regimen_impostos=regimen_impostos
        )

        db.session.add(nova_factura)
        try:
            db.session.commit()
            flash('Factura creada exitosamente.', 'success')
            return redirect(url_for('llistar_factures'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la factura.', 'danger')
            return redirect(url_for('create_factura'))

    comunitats = Comunidad.query.order_by(Comunidad.nombre.asc()).all()
    return render_template('create_factura.html', comunitats=comunitats)

@app.context_processor
def utility_processor():
    return {'now': datetime.now()}

@app.route('/start_pause', methods=['POST'])
@login_required
def start_pause():
    active_record = TimeRecord.query.filter_by(user_id=current_user.id, check_out=None).first()
    if not active_record:
        flash('No tienes un registro activo para pausar.', 'warning')
        return redirect(url_for('index'))
    open_pause = PauseRecord.query.filter_by(time_record_id=active_record.id, pause_end=None).first()
    if open_pause:
        flash('Ya tienes una pausa activa.', 'warning')
        return redirect(url_for('index'))
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    accuracy = request.form.get('accuracy')
    pause = PauseRecord(
        time_record_id=active_record.id,
        pause_start=datetime.now(),
        pause_date=datetime.now().date(),  # Assigna el dia de la pausa
        pause_latitude=float(latitude) if latitude else None,
        pause_longitude=float(longitude) if longitude else None,
        pause_accuracy=float(accuracy) if accuracy else None
    )
    db.session.add(pause)
    db.session.commit()
    flash('Pausa iniciada.', 'success')
    return redirect(url_for('index'))

@app.route('/end_pause', methods=['POST'])
@login_required
def end_pause():
    active_record = TimeRecord.query.filter_by(user_id=current_user.id, check_out=None).first()
    if not active_record:
        flash('No tienes un registro activo.', 'warning')
        return redirect(url_for('index'))
    open_pause = PauseRecord.query.filter_by(time_record_id=active_record.id, pause_end=None).first()
    if not open_pause:
        flash('No tienes una pausa activa.', 'warning')
        return redirect(url_for('index'))
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    accuracy = request.form.get('accuracy')
    open_pause.pause_end = datetime.now()
    open_pause.pause_latitude = float(latitude) if latitude else open_pause.pause_latitude
    open_pause.pause_longitude = float(longitude) if longitude else open_pause.pause_longitude
    open_pause.pause_accuracy = float(accuracy) if accuracy else open_pause.pause_accuracy
    db.session.commit()
    flash('Pausa finalitzada.', 'success')
    return redirect(url_for('index'))

@app.route('/report_incident', methods=['POST'])
@login_required
def report_incident():
    active_record = TimeRecord.query.filter_by(user_id=current_user.id, check_out=None).first()
    if not active_record:
        flash('Has d\'estar registrat per reportar una incidència.', 'warning')
        return redirect(url_for('index'))
    category = request.form.get('category')
    description = request.form.get('description')
    time = request.form.get('time')
    # Si l'usuari no edita l'hora, agafem la d'ara
    if not time:
        time = datetime.now(ZoneInfo("Europe/Madrid")).time().strftime('%H:%M:%S')
    incidencia = Incidencia(
        user_id=current_user.id,
        time_record_id=active_record.id,
        date=datetime.now(ZoneInfo("Europe/Madrid")).date(),
        time=datetime.strptime(time, '%H:%M:%S').time(),
        category=category,
        description=description
    )
    db.session.add(incidencia)
    db.session.commit()
    flash('Incidència registrada correctament.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
