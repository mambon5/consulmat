from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from flask_login import login_required, current_user
from app.models import Empresa, User, Treballador, Comunidad, Pagador
from app import db, bcrypt, mail
from datetime import datetime
import random
import pycountry
from utils import get_serializer
from flask_mail import Message

empresa_bp = Blueprint("empresa", __name__)

def send_empresa_registration_email(email, link):
    """
    Envia l'enllaç de registre d'empresa amb token a l'email.
    """
    msg = Message(
        subject='Enllaç per registrar la teva empresa',
        sender=mail.sender,
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

def create_empresa_logic(template_name='create_empresa.html', page_title="Crear Empresa"):
    email_sent = False

    if request.method == 'POST':
        # POST de verificació del codi email
        if 'email_code' in request.form:
            reg_data = session.get('empresa_reg_data')
            if not reg_data:
                flash('Sesión expirada. Por favor, regístrate de nuevo.', 'danger')
                return redirect(request.url)

            if request.form['email_code'] == reg_data['email_code']:
                hashed_password = bcrypt.generate_password_hash(reg_data['password']).decode('utf-8')
                nova_empresa = Empresa(
                    nom=reg_data['nom_empresa'],
                    numero_fiscal=reg_data['numero_fiscal'],
                    adreca=reg_data['adreca'],
                    correu_gerent=reg_data['correu_gerent'],
                    telefon_gerent=reg_data['telefon_gerent'],
                    password=hashed_password
                )
                db.session.add(nova_empresa)
                db.session.commit()

                session.pop('empresa_reg_data', None)
                flash('Empresa creada correctamente. Ahora puedes registrar el primer administrador.', 'success')
                return redirect(url_for('auth.register_first_admin', empresa_id=nova_empresa.id))
            else:
                flash('Código de verificación incorrecto.', 'danger')
                email_sent = True
                return render_template(template_name, email_sent=email_sent, page_title=page_title)

        # Primer pas: registre empresa
        nom_empresa = request.form.get('nom_empresa')
        numero_fiscal = request.form.get('numero_fiscal')
        adreca = request.form.get('adreca')
        correu_gerent = request.form.get('correu_gerent')
        telefon_gerent = request.form.get('telefon_gerent')
        password = request.form.get('password')

        # Validar unicitat NIF
        if Empresa.query.filter_by(numero_fiscal=numero_fiscal).first():
            flash('Ya existe una empresa con ese número fiscal.', 'danger')
            return render_template(template_name, page_title=page_title)

        # Generar codi de verificació
        email_code = str(random.randint(100000, 999999))

        session['empresa_reg_data'] = {
            'nom_empresa': nom_empresa,
            'numero_fiscal': numero_fiscal,
            'adreca': adreca,
            'correu_gerent': correu_gerent,
            'telefon_gerent': telefon_gerent,
            'password': password,
            'email_code': email_code
        }

        from app.routes.auth import send_verification_email
        send_verification_email(correu_gerent, email_code)
        email_sent = True
        flash('Se ha enviado un email de verificación al correo del gerente.', 'info')
        return render_template(template_name, email_sent=email_sent, page_title=page_title)

    # GET
    return render_template(template_name, email_sent=email_sent, page_title=page_title)

    return render_template(template_name, email_sent=email_sent, page_title=page_title)

@empresa_bp.route("/create_empresa", methods=["GET","POST"])
def create_empresa():
    return create_empresa_logic()

@empresa_bp.route('/generate_empresa_link', methods=['GET', 'POST'])
@login_required
def generate_empresa_link():
    # ✅ Només admins de l'empresa amb id=1
    if current_user.role != 'admin' or current_user.empresa_id != 1:
        flash("No tens permisos per generar enllaços.", "danger")
        return redirect(url_for('fichajes.index'))

    if request.method == 'POST':
        email_destinatari = request.form['email']

        # Serialitzador per generar token únic
        s = get_serializer()
        token = s.dumps({"action": "create_empresa"})
        link = url_for('empresa.create_empresa_with_token', token=token, _external=True)

        # Enviar email amb el link
        send_empresa_registration_email(email_destinatari, link)

        flash(f"S'ha enviat un enllaç de registre a {email_destinatari}", "success")
        return redirect(url_for('fichajes.index'))

    return render_template('generate_empresa_link.html')

@empresa_bp.route('/create_empresa_with_token/<token>', methods=['GET', 'POST'])
def create_empresa_with_token(token):
    s = get_serializer()
    try:
        data = s.loads(token, max_age=86400)  # token vàlid 24h
        if data.get("action") != "create_empresa":
            flash("Enllaç invàlid.", "danger")
            return redirect(url_for('auth.login'))
    except Exception:
        flash("L'enllaç no és vàlid o ha caducat.", "danger")
        return redirect(url_for('auth.login'))

    # Reutilitzar la lògica de creació d'empresa
    return create_empresa_logic(template_name='create_empresa.html', page_title="Registrar Empresa")

@empresa_bp.route('/create_treballador/<int:empresa_id>', methods=['GET', 'POST'])
@login_required
def create_treballador(empresa_id):
    if current_user.role != 'admin':
        flash('No tienes permisos para crear trabajadores.', 'danger')
        return redirect(url_for('fichajes.index'))

    paisos = [{'code': country.alpha_2, 'name': country.name} for country in pycountry.countries]

    extra_fields = None
    if request.method == 'POST':
        extra_fields = {
            "departament": request.form.get('departament'),
            "adreca": request.form.get('adreca'),
            "ciutat": request.form.get('ciutat'),
            "codi_postal": int(request.form.get('codi_postal')) if request.form.get('codi_postal') else None,
            "sexe": request.form.get('sexe'),
            "nacionalitat": request.form.get('nacionalitat'),
            "edat": int(request.form.get('edat')) if request.form.get('edat') else None,
            "carnet_conduir": request.form.get('carnet_conduir'),
            "vehicle_propi": request.form.get('vehicle_propi'),
            "created_at": datetime.utcnow()
        }

    from app.routes.auth import create_user_logic
    return create_user_logic(role="employee", empresa_id=empresa_id,
                             extra_fields=extra_fields,
                             template_name='create_treballador.html',
                             page_title="Crear Treballador",
                             show_role_dropdown=False)  # ✅ no mostrar dropdown

@empresa_bp.route('/create_comunitat', methods=['GET', 'POST'])
@login_required
def create_comunitat():
    if current_user.role != 'admin':
        flash('No tienes permisos para crear comunidades.', 'danger')
        return redirect(url_for('fichajes.index'))

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
            return redirect(url_for('empresa.create_comunitat'))

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
            return redirect(url_for('fichajes.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la comunidad: {str(e)}', 'danger')
            return redirect(url_for('empresa.create_comunitat'))

    # Si no és POST, renderitzem el formulari
    return render_template('create_comunitat.html')

@empresa_bp.route('/create_pagador', methods=['GET', 'POST'])
@login_required
def create_pagador():
    if current_user.role != 'admin':
        flash('No tens permisos per crear pagadors.', 'danger')
        return redirect(url_for('fichajes.index'))

    if request.method == 'POST':
        nom_pagador = request.form.get('nom_pagador')
        telefon = request.form.get('telefon')
        email = request.form.get('email')
        direccio = request.form.get('direccio')
        ciutat = request.form.get('ciutat')
        codi_postal = request.form.get('codi_postal')

        if Pagador.query.filter_by(email=email).first():
            flash('Ja existeix un pagador amb aquest correu.', 'danger')
            return redirect(url_for('empresa.create_pagador'))

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
            return redirect(url_for('empresa.pagadors'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el pagador: {str(e)}', 'danger')
            return redirect(url_for('empresa.create_pagador'))

    return render_template('create_pagador.html')

@empresa_bp.route('/pagadors')
@login_required
def pagadors():
    if current_user.role != 'admin':
        flash('No tens permisos per veure aquesta pàgina.', 'danger')
        return redirect(url_for('fichajes.index'))

    pagadors = Pagador.query.order_by(Pagador.nom_pagador.asc()).all()
    return render_template('llistat_pagadors.html', pagadors=pagadors)

@empresa_bp.route('/usuaris')
@login_required
def usuaris():
    if current_user.role != 'admin':
        flash('No tens permisos per accedir a aquesta pàgina.', 'danger')
        return redirect(url_for('fichajes.index'))

    usuaris = User.query.order_by(User.name.asc()).all()
    return render_template('llistat_usuaris.html', usuaris=usuaris)

@empresa_bp.route('/treballadors')
@login_required
def treballadors():
    treballadors = Treballador.query.all()
    return render_template("llistat_treballadors.html", treballadors=treballadors)

@empresa_bp.route('/usuari/<int:user_id>')
@login_required
def usuari(user_id):
    user = User.query.get_or_404(user_id)
    treballador = user.treballador if user.role == 'employee' else None
    return render_template('perfil_usuari.html', user=user, treballador=treballador)

@empresa_bp.route('/comunitats')
@login_required
def comunitats():
    if current_user.role != 'admin':
        flash('No tens permisos per accedir a aquesta pàgina.', 'danger')
        return redirect(url_for('fichajes.index'))

    comunitats = Comunidad.query.order_by(Comunidad.fecha_alta.asc()).all()
    return render_template('llistat_comunitats.html', comunitats=comunitats)
