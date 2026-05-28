from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_babel import _
from flask_login import login_required, current_user
from app.models import db, User, Treballador, TimeRecord, PauseRecord, Incidencia, EventoLaboral, Empresa, Calendari
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from calendar import monthrange
from sqlalchemy import func

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
@login_required
def admin_panel():
    if current_user.role != "admin":
        return _("No autorizado"), 403
    return render_template("create_admin.html")

@admin_bp.route("/admin/dashboard")
@login_required
def dashboard():
    if current_user.role != "admin":
        return "No autorizado", 403
    
    empresa_id = current_user.empresa_id
    treballadors = Treballador.query.filter_by(empresa_id=empresa_id).all()
    
    workers_status = []
    
    today = datetime.now(ZoneInfo("Europe/Madrid")).date()
    
    # Últimes 10 solicitudes de la empresa
    solicitudes = EventoLaboral.query.join(Treballador).filter(
        Treballador.empresa_id == empresa_id
    ).order_by(EventoLaboral.fecha_solicitud.desc()).limit(10).all()

    # Tots els events per al calendari
    calendar_events = EventoLaboral.query.join(Treballador).filter(
        Treballador.empresa_id == empresa_id
    ).all()
    
    events_data = []
    for ev in calendar_events:
        nom = ev.treballador.user.name or ev.treballador.user.username
        title = f"{nom} - {ev.tipo_evento.replace('_', ' ').title()}"
        if not ev.aprovada:
            title += _(" (Pendent)")
            
        color = '#28a745' if ev.aprovada else '#ffc107'
        if not ev.aprovada:
            text_color = '#000'
        else:
            text_color = '#fff'
            
        events_data.append({
            'id': ev.id,
            'title': title,
            'start': ev.fecha.isoformat(),
            'allDay': True,
            'backgroundColor': color,
            'borderColor': color,
            'textColor': text_color
        })

    # Incidències recents de la empresa
    start_of_month = today.replace(day=1)
    incidencias = Incidencia.query.join(User).filter(
        User.empresa_id == empresa_id,
        Incidencia.date >= start_of_month
    ).order_by(Incidencia.date.desc(), Incidencia.time.desc()).all()

    for t in treballadors:
        user_id = t.id_usuari
        active_record = TimeRecord.query.filter_by(user_id=user_id, check_out=None).first()
        status = 'red'
        if active_record:
            active_pause = PauseRecord.query.filter_by(time_record_id=active_record.id, pause_end=None).first()
            if active_pause:
                status = 'yellow'
            else:
                status = 'green'
                
        workers_status.append({
            'treballador': t,
            'user': t.user,
            'status': status
        })

    return render_template(
        "admin_dashboard.html",
        workers_status=workers_status,
        solicitudes=solicitudes,
        incidencias=incidencias,
        events_data=events_data,
        today=today
    )

@admin_bp.route("/admin/api/solicitudes")
@login_required
def api_solicitudes():
    if current_user.role != "admin":
        return jsonify({"error": "No autorizado"}), 403
        
    offset = request.args.get('offset', type=int, default=0)
    limit = 10
    
    solicitudes = EventoLaboral.query.join(Treballador).filter(
        Treballador.empresa_id == current_user.empresa_id
    ).order_by(EventoLaboral.fecha_solicitud.desc()).offset(offset).limit(limit).all()
    
    data = []
    for s in solicitudes:
        data.append({
            'nom': s.treballador.user.name or s.treballador.user.username,
            'data_solicitud': s.fecha_solicitud.strftime('%d/%m/%Y') if s.fecha_solicitud else '-',
            'data_abscencia': s.fecha.strftime('%d/%m/%Y'),
            'tipus': s.tipo_evento.replace('_', ' ').title(),
            'aprovada': s.aprovada
        })
        
    return jsonify({'solicitudes': data})

@admin_bp.route("/admin/api/stats")
@login_required
def api_stats():
    if current_user.role != "admin":
        return jsonify({"error": "No autorizado"}), 403
        
    year = request.args.get('year', type=int, default=datetime.now(ZoneInfo("Europe/Madrid")).year)
    month = request.args.get('month', type=int, default=datetime.now(ZoneInfo("Europe/Madrid")).month)
    
    empresa_id = current_user.empresa_id
    treballadors = Treballador.query.filter_by(empresa_id=empresa_id).all()
    
    # calcular dates
    start_date = datetime(year, month, 1)
    end_date = start_date.replace(day=monthrange(year, month)[1], hour=23, minute=59, second=59)
    
    stats = []
    for t in treballadors:
        user_id = t.id_usuari
        records = TimeRecord.query.filter(
            TimeRecord.user_id == user_id,
            TimeRecord.check_in >= start_date,
            TimeRecord.check_in <= end_date
        ).all()
        dies_treb = len(set(r.check_in.date() for r in records))
        
        events = EventoLaboral.query.filter(
            EventoLaboral.id_treballador == t.id_treballador,
            EventoLaboral.fecha >= start_date.date(),
            EventoLaboral.fecha <= end_date.date(),
            EventoLaboral.aprovada == True
        ).all()
        
        dies_festa = 0
        dies_baixa = 0
        
        for ev in events:
            if ev.tipo_evento in ['vacances', 'assumptes_propis', 'festivo_nacional', 'festivo_autonomico', 'festivo_local']:
                dies_festa += 1
            elif ev.tipo_evento == 'baixa_medica':
                dies_baixa += 1
                
        stats.append({
            'id': t.id_treballador,
            'nom': t.user.name or t.user.username,
            'dies_treballats': dies_treb,
            'dies_festa': dies_festa,
            'dies_baixa': dies_baixa
        })
        
    return jsonify({'stats': stats})

@admin_bp.route("/admin/worker/<int:id_treballador>")
@login_required
def worker_detail(id_treballador):
    if current_user.role != "admin":
        return _("No autorizado"), 403
        
    treballador = Treballador.query.get_or_404(id_treballador)
    
    # Check that is from the same company
    if treballador.empresa_id != current_user.empresa_id:
        return _("No autorizado"), 403
        
    # Get user details for this worker
    user = treballador.user
    
    # Status
    active_record = TimeRecord.query.filter_by(user_id=user.id, check_out=None).first()
    status = 'red'
    if active_record:
        active_pause = PauseRecord.query.filter_by(time_record_id=active_record.id, pause_end=None).first()
        status = 'yellow' if active_pause else 'green'
        
    # Fichajes (últimes 50)
    records = TimeRecord.query.filter_by(user_id=user.id).order_by(TimeRecord.check_in.desc()).limit(50).all()
    
    # Incidencias
    incidencias = Incidencia.query.filter_by(user_id=user.id).order_by(Incidencia.date.desc(), Incidencia.time.desc()).limit(50).all()
    
    # Eventos laborales (calendario permisos)
    eventos = EventoLaboral.query.filter_by(id_treballador=id_treballador).order_by(EventoLaboral.fecha.desc()).all()
    
    return render_template(
        "admin_worker_detail.html",
        treballador=treballador,
        user=user,
        status=status,
        records=records,
        incidencias=incidencias,
        eventos=eventos
    )
