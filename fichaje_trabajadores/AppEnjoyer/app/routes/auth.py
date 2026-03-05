from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from app.models import User, Empresa, Treballador
from app import db, bcrypt, login_manager, mail
import random
from datetime import datetime

auth_bp = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def send_verification_email(email, code):
    msg = Message('Código de verificación', sender=mail.sender, recipients=[email])
    msg.body = f'Tu código de verificación es: {code}'
    mail.send(msg)

def create_user_logic(role="employee", empresa_id=None, extra_fields=None,
                      template_name='create_user.html', page_title="Crear Usuario",
                      show_role_dropdown=True, skip_verification=False, prefilled_email=None, **kwargs):
    email_sent = False

    empresa = None
    if empresa_id:
        empresa = Empresa.query.get(empresa_id)
        if empresa:
            page_title = f"{page_title} - {empresa.nom}"

    if request.method == 'POST':
        # POST de verificació del codi email
        if 'email_code' in request.form:
            reg_data = session.get('reg_data')
            if not reg_data:
                flash('Sesión expirada. Por favor, regístrate de nuevo.', 'danger')
                return redirect(request.url)
            if request.form['email_code'] == reg_data['email_code']:
                return finalize_user_creation(reg_data, empresa_id, extra_fields)
            else:
                flash('Código de verificación incorrecto.', 'danger')
                email_sent = True
                return render_template(template_name, email_sent=email_sent,
                                       page_title=page_title, empresa=empresa,
                                       role=role, show_role_dropdown=show_role_dropdown,
                                       prefilled_email=prefilled_email, **kwargs)

        # Primer pas: registre
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        # Opcional: contrasenya de l'empresa (pel primer admin)
        empresa_password = request.form.get('empresa_password')

        # Capturar el rol del dropdown si s'usa
        role = request.form.get('role', role)

        # Validacions
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado.', 'danger')
            return render_template(template_name, username=username, name=name, phone=phone, email=email,
                                   page_title=page_title, empresa=empresa,
                                   role=role, show_role_dropdown=show_role_dropdown,
                                   prefilled_email=prefilled_email, extra_fields=extra_fields, **kwargs)

        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.', 'danger')
            return render_template(template_name, name=name, email=email, phone=phone, username=username,
                                   page_title=page_title, empresa=empresa,
                                   role=role, show_role_dropdown=show_role_dropdown,
                                   prefilled_email=prefilled_email, extra_fields=extra_fields, **kwargs)
        
        # Validar contrasenya d'empresa si es demana
        if empresa and empresa_password:
            if not bcrypt.check_password_hash(empresa.password, empresa_password):
                flash('La contraseña de la empresa es incorrecta.', 'danger')
                return render_template(template_name, username=username, name=name, phone=phone,
                                       page_title=page_title, empresa=empresa, email=email,
                                       role=role, show_role_dropdown=show_role_dropdown,
                                       prefilled_email=prefilled_email, extra_fields=extra_fields, **kwargs)

        reg_data = {
            'username': username,
            'password': password,
            'name': name,
            'email': email,
            'phone': phone,
            'role': role,
            'extra_fields': extra_fields
        }

        if skip_verification:
            return finalize_user_creation(reg_data, empresa_id, extra_fields)

        # Generar codi de verificació
        email_code = str(random.randint(100000, 999999))
        reg_data['email_code'] = email_code
        
        # 🔹 GUARDEM EL REG_DATA A LA SESSIÓ
        session['reg_data'] = reg_data

        send_verification_email(email, email_code)
        email_sent = True
        flash('Se ha enviado un email de verificación a tu correo.', 'info')
        return render_template(template_name, email_sent=email_sent,
                               page_title=page_title, empresa=empresa,
                               role=role, show_role_dropdown=show_role_dropdown,
                               prefilled_email=prefilled_email, **kwargs)

    # GET
    return render_template(template_name, email_sent=email_sent,
                           page_title=page_title, empresa=empresa,
                           role=role, show_role_dropdown=show_role_dropdown,
                           prefilled_email=prefilled_email, **kwargs)

def finalize_user_creation(reg_data, empresa_id, extra_fields):
    hashed_password = bcrypt.generate_password_hash(reg_data['password']).decode('utf-8')
    user = User(
        username=reg_data['username'],
        password=hashed_password,
        name=reg_data['name'],
        email=reg_data['email'],
        phone=reg_data['phone'],
        email_verified=True,
        role=reg_data['role'],
        data_consent=True,
        consent_date=datetime.utcnow(),
        data_retention_days=1460,
        empresa_id=empresa_id
    )
    db.session.add(user)
    db.session.commit()

    session_extra_fields = reg_data.get('extra_fields', {})
    if reg_data['role'] == "employee":
        fields_to_use = session_extra_fields if session_extra_fields else extra_fields
        
        if fields_to_use:
            if 'created_at' in fields_to_use and isinstance(fields_to_use['created_at'], str):
                 try:
                     fields_to_use['created_at'] = datetime.fromisoformat(fields_to_use['created_at'])
                 except:
                     fields_to_use['created_at'] = datetime.utcnow()

            nou_treballador = Treballador(
                id_usuari=user.id,
                empresa_id=empresa_id,
                **fields_to_use
            )
            db.session.add(nou_treballador)
            db.session.commit()

    session.pop('reg_data', None)
    # Netejar flags de registre d'empresa si existien
    session.pop('admin_email_verified', None)
    session.pop('admin_prefill_email', None)

    flash(f'Cuenta creada correctamente como {reg_data["role"]}.', 'success')
    return redirect(url_for('fichajes.index'))

@auth_bp.route('/create_user/<int:empresa_id>', methods=['GET', 'POST'])
@login_required
def create_user(empresa_id):
    return create_user_logic(role="employee", empresa_id=empresa_id,
                             template_name='create_user.html',
                             page_title="Crear Usuario",
                             show_role_dropdown=True)

@auth_bp.route('/create_admin/<int:empresa_id>', methods=['GET', 'POST'])
@login_required
def create_admin(empresa_id):
    if current_user.role != 'admin':
        flash('No tienes permisos para crear administradores.', 'danger')
        return redirect(url_for('fichajes.index'))

    return create_user_logic(role="admin", empresa_id=empresa_id,
                             template_name='create_user.html',
                             page_title="Crear Administrador",
                             show_role_dropdown=False)

@auth_bp.route('/register_first_admin/<int:empresa_id>', methods=['GET', 'POST'])
def register_first_admin(empresa_id):
    skip_verification = session.get('admin_email_verified', False)
    prefilled_email = session.get('admin_prefill_email')
    
    return create_user_logic(role="admin", empresa_id=empresa_id,
                             template_name='register_first_admin.html',
                             page_title="Registrar Primer Administrador",
                             show_role_dropdown=False,
                             skip_verification=skip_verification,
                             prefilled_email=prefilled_email)

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('fichajes.index'))
        
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Por favor, introduce usuario y contraseña.', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash(f'Bienvenido/a, {user.name}', 'success')
            return redirect(url_for('fichajes.index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            
    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
