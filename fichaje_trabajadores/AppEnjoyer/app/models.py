from . import db
from flask_login import UserMixin
from datetime import datetime
from zoneinfo import ZoneInfo
from zoneinfo import ZoneInfo



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empreses.id'), nullable=False)

    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
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

class Empresa(db.Model):
    __tablename__ = 'empreses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(120), nullable=False)
    nom = db.Column(db.String(255), nullable=False, unique=True)
    numero_fiscal = db.Column(db.String(50), nullable=False, unique=True)
    adreca = db.Column(db.String(255), nullable=True)
    correu_gerent = db.Column(db.String(255), nullable=True)
    telefon_gerent = db.Column(db.String(20), nullable=True)
    data_registre = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacions
    usuaris = db.relationship('User', backref='empresa', lazy=True)
    treballadors = db.relationship('Treballador', backref='empresa', lazy=True)



class Treballador(db.Model):
    __tablename__ = 'treballadors'

    id_treballador = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuari = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empreses.id'), nullable=False)

    departament = db.Column(
        db.Enum('parkings', 'comunitats', 'oficines', 'manteniment', 'administració', name='departament_enum'),
        nullable=False
    )
    adreca = db.Column(db.String(255), nullable=True)
    ciutat = db.Column(db.String(100), nullable=True)
    codi_postal = db.Column(db.Integer, nullable=True)
    sexe = db.Column(db.Enum('f', 'm', 'no', name='sexe_enum'), nullable=True)
    nacionalitat = db.Column(db.String(100), nullable=True)
    edat = db.Column(db.Integer, nullable=True)
    carnet_conduir = db.Column(db.Enum('si', 'no', name='carnet_conduir_enum'), nullable=True)
    vehicle_propi = db.Column(db.Enum('si', 'no', name='vehicle_propi_enum'), nullable=True)
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
    hora_inicio = db.Column(db.Time, nullable=True)
    hora_fin = db.Column(db.Time, nullable=True)
    tipo_evento = db.Column(
        db.Enum(
            'trabajo',
            'festivo_nacional',
            'festivo_autonomico',
            'festivo_local',
            'vacances',   # 🔹 AFEGIT
            'assumptes_propis',
            'baixa_medica',
            'teletreball',
            name='tipo_evento_enum'
        ),
        nullable=False,
        default='trabajo'
    )

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
