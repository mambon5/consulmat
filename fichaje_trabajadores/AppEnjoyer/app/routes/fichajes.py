from flask import Blueprint, render_template, redirect, url_for, request, flash, send_file
from flask_login import login_required, current_user
from models import TimeRecord, Incidencia, PauseRecord
from app import db
from datetime import datetime
from zoneinfo import ZoneInfo
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from timedelta import timedelta

fichajes_bp = Blueprint("fichajes", __name__)

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

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

@fichajes_bp.route("/")
@login_required
def index():
    records = TimeRecord.query.filter_by(user_id=current_user.id).order_by(TimeRecord.check_in.desc()).all()
    active_record = TimeRecord.query.filter_by(user_id=current_user.id, check_out=None).first()
    today = datetime.now(ZoneInfo("Europe/Madrid")).date()
    today_incidencies = Incidencia.query.filter_by(user_id=current_user.id, date=today).order_by(Incidencia.time.desc()).all()
    return render_template('index.html', records=records, active_record=active_record, today_incidencies=today_incidencies)


    return render_template('index.html', records=records, active_record=active_record, today_incidencies=today_incidencies)

@fichajes_bp.route("/check_in", methods=['POST'])
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
    return redirect(url_for('fichajes.index'))

@fichajes_bp.route("/check_out", methods=['POST'])
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
    return redirect(url_for('fichajes.index'))

@fichajes_bp.route('/generate_report', methods=['GET', 'POST'])
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

@fichajes_bp.route('/start_pause', methods=['POST'])
@login_required
def start_pause():
    active_record = TimeRecord.query.filter_by(user_id=current_user.id, check_out=None).first()
    if not active_record:
        flash('No tienes un registro activo para pausar.', 'warning')
        return redirect(url_for('fichajes.index'))
    open_pause = PauseRecord.query.filter_by(time_record_id=active_record.id, pause_end=None).first()
    if open_pause:
        flash('Ya tienes una pausa activa.', 'warning')
        return redirect(url_for('fichajes.index'))
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
    return redirect(url_for('fichajes.index'))

@fichajes_bp.route('/end_pause', methods=['POST'])
@login_required
def end_pause():
    active_record = TimeRecord.query.filter_by(user_id=current_user.id, check_out=None).first()
    if not active_record:
        flash('No tienes un registro activo.', 'warning')
        return redirect(url_for('fichajes.index'))
    open_pause = PauseRecord.query.filter_by(time_record_id=active_record.id, pause_end=None).first()
    if not open_pause:
        flash('No tienes una pausa activa.', 'warning')
        return redirect(url_for('fichajes.index'))
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    accuracy = request.form.get('accuracy')
    open_pause.pause_end = datetime.now()
    open_pause.pause_latitude = float(latitude) if latitude else open_pause.pause_latitude
    open_pause.pause_longitude = float(longitude) if longitude else open_pause.pause_longitude
    open_pause.pause_accuracy = float(accuracy) if accuracy else open_pause.pause_accuracy
    db.session.commit()
    flash('Pausa finalitzada.', 'success')
    return redirect(url_for('fichajes.index'))

@fichajes_bp.route('/report_incident', methods=['POST'])
@login_required
def report_incident():
    active_record = TimeRecord.query.filter_by(user_id=current_user.id, check_out=None).first()
    if not active_record:
        flash('Has d\'estar registrat per reportar una incidència.', 'warning')
        return redirect(url_for('fichajes.index'))
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
    return redirect(url_for('fichajes.index'))
