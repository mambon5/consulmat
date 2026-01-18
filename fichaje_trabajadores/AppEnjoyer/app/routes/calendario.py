from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import EventoLaboral, HorarioLaboral, Treballador
from app import db
from datetime import datetime, date
from calendar import monthrange

calendario_bp = Blueprint("calendario", __name__)

@calendario_bp.route("/calendario-laboral")
@login_required
def calendario_laboral():
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
        color = "#1976d2"  # blau = treball
        if "festivo" in evento.tipo_evento:
            color = "#e53935"  # vermell = festiu
        elif evento.tipo_evento == "vacances":
            color = "#43a047"  # verd = vacances

        eventos.append({
            "title": evento.tipo_evento.replace('_', ' ').capitalize(),
            "start": evento.fecha.isoformat(),
            "allDay": True if not evento.hora_inicio else False,
            "color": color
    })


    # Horarios recurrentes (Lunes a Viernes, etc.)
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



    absencies = EventoLaboral.query.filter_by(id_treballador=treballador.id_treballador).all()
    tipus_abs = ['vacances', 'baixa_medica', 'assumptes_propis']

    stats = {t: 0 for t in tipus_abs}
    for a in absencies:
        if a.tipo_evento in stats:
            stats[a.tipo_evento] += 1

    # valors de referència
    lim = {'vacances': 30, 'baixa_medica': 90, 'assumptes_propis': 3}
    restants = {t: lim[t] - stats[t] for t in stats}

    return render_template(
        'calendari.html',
        eventos=eventos,
        treballadors=treballadors,
        treballador_seleccionat=treballador,
        stats=stats,
        restants=restants
    )

@calendario_bp.route('/api/absencia', methods=['POST'])
@login_required
def crear_absencia():
    data = request.get_json(silent=True)
    if not data or 'fecha' not in data or 'tipo_evento' not in data:
        return jsonify({"error": "Falten dades (fecha o tipo_evento)"}), 400

    try:
        fecha = datetime.strptime(data['fecha'][:10], '%Y-%m-%d').date()
        tipo_evento = data['tipo_evento']

        # ⚙️ teleworking és compatible amb altres absències
        if tipo_evento != 'teletreball':
            existent = EventoLaboral.query.filter_by(
                id_treballador=current_user.treballador.id_treballador,
                fecha=fecha
            ).filter(EventoLaboral.tipo_evento != 'teletreball').first()
            if existent:
                return jsonify({"error": "Ja existeix una absència per aquest dia"}), 400
        
        if tipo_evento == 'teletreball':
            existent = EventoLaboral.query.filter_by(
                id_treballador=current_user.treballador.id_treballador,
                fecha=fecha
            ).filter(EventoLaboral.tipo_evento == 'teletreball').first()
            if existent:
                return jsonify({"error": "Ja existeix un teletreball per aquest dia"}), 400

        dia = EventoLaboral(
            id_treballador=current_user.treballador.id_treballador,
            id_comunitat=data.get('id_comunitat', 1),
            fecha=fecha,
            tipo_evento=tipo_evento
        )
        db.session.add(dia)
        db.session.commit()
        return jsonify({"status": "ok", "message": f"{tipo_evento.capitalize()} afegit per {fecha}"})
    except Exception as e:
        db.session.rollback()
        print("❌ Error a /api/absencia:", e)
        return jsonify({"error": str(e)}), 500

@calendario_bp.route('/api/vacances/<int:event_id>', methods=['DELETE'])
@login_required
def eliminar_vacances(event_id):
    evento = EventoLaboral.query.get_or_404(event_id)
    if evento.id_treballador == current_user.treballador.id_treballador and evento.tipo_evento == 'vacances':
        db.session.delete(evento)
        db.session.commit()
        return jsonify({"status": "ok", "message": "Vacances eliminades"})
    return jsonify({"status": "error", "message": "No autoritzat"}), 403

@calendario_bp.route("/calendari")
@login_required
def calendari():
    return render_template("calendari.html")
