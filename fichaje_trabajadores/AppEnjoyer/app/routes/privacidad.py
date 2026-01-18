from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import DataProcessingConsent, TimeRecord
from app import db
from datetime import datetime

privacidad_bp = Blueprint("privacidad", __name__)

def require_data_consent():
    # Solo para usuarios autenticados y rutas privadas
    if current_user.is_authenticated:
        # Excluye rutas públicas y la propia ruta de consentimiento
        allowed_routes = ['privacidad.data_consent', 'auth.logout', 'privacidad.privacy_policy', 'privacidad.aviso_legal', 'static']
        if not current_user.data_consent and request.endpoint not in allowed_routes:
            return redirect(url_for('privacidad.data_consent'))

@privacidad_bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@privacidad_bp.route('/data-consent', methods=['GET', 'POST'])
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
        return redirect(url_for('privacidad.privacy_settings'))
        
    return render_template('data_consent.html')

@privacidad_bp.route('/privacy-settings')
@login_required
def privacy_settings():
    return render_template('privacy_settings.html')

@privacidad_bp.route('/aviso-legal')
def aviso_legal():
    return render_template('aviso_legal.html')

@privacidad_bp.route('/export-data')
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

@privacidad_bp.route('/delete-data', methods=['POST'])
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
        from flask_login import logout_user
        logout_user()
        flash('Tu cuenta y todos tus datos han sido eliminados', 'success')
        return redirect(url_for('auth.login'))
    
    flash('Confirmación requerida para eliminar datos', 'error')

@privacidad_bp.route("/privacy")
@login_required
def privacy():
    return render_template("privacy_settings.html")
